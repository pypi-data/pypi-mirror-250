"""Common utils to support neos cli applications."""
import dataclasses
import typing
from csv import DictWriter
from io import StringIO

from fastapi import FastAPI
from yoyo import get_backend, read_migrations
from yoyo.migrations import topological_sort


def migration_upgrade(postgres_dsn: str) -> None:
    backend = get_backend(postgres_dsn)

    migrations = read_migrations("migrations")

    with backend.lock():
        # Apply any outstanding migrations
        backend.apply_migrations(backend.to_apply(migrations))


def migration_downgrade(postgres_dsn: str, count: typing.Union[int, None] = 1) -> None:
    backend = get_backend(postgres_dsn)

    migrations = backend.to_rollback(
        read_migrations("migrations"),
    )
    if count:
        migrations = migrations[:count]

    with backend.lock():
        # Rollback selected migrations (default is latest)
        backend.rollback_migrations(migrations, force=True)


def migration_history(postgres_dsn: str) -> typing.Generator[typing.Tuple[str, str], None, None]:
    backend = get_backend(postgres_dsn)
    migrations = read_migrations("migrations")

    with backend.lock():
        migrations = migrations.__class__(topological_sort(migrations))
        applied = backend.to_rollback(migrations)

    return (("A" if m in applied else " ", m.id) for m in migrations)


@dataclasses.dataclass
class PermissionPair:
    """Permission pair."""

    action: str
    resource: str


@dataclasses.dataclass
class FormattedRoute:
    """Formatted route."""

    methods: str
    path: str
    permission_pairs: typing.List[PermissionPair]


class RoutesPrinter:
    """Routes printer."""

    def __init__(self, app: FastAPI, ignore_routes: typing.List[str]) -> None:
        self.routes = self._get_routes(app, ignore_routes)

    @staticmethod
    def _get_routes(app: FastAPI, ignore_routes: typing.List[str]) -> typing.List[FormattedRoute]:
        routes = []
        for route in app.routes:
            if route.path in ignore_routes:
                continue

            methods = ", ".join(list(route.methods))

            path = route.path

            permission_pairs = []
            if hasattr(route, "openapi_extra") and route.openapi_extra is not None:
                actions = []
                resources = []
                for key in sorted(route.openapi_extra):
                    if key.startswith("x-iam-action"):
                        actions.append(route.openapi_extra[key])
                    if key.startswith("x-iam-resource"):
                        resources.append(route.openapi_extra[key])

                permission_pairs = [PermissionPair(a, r) for a, r in zip(actions, resources)]

            routes.append(FormattedRoute(methods, path, permission_pairs))

        return routes

    def echo(self, echo_fn: typing.Callable) -> None:
        """Print routes to console."""
        for route in self.routes:
            echo_fn(f"{route.methods:<10}{route.path}")
            for permission_pair in route.permission_pairs:
                echo_fn("{:<12}action:   {}".format("", permission_pair.action))
                echo_fn("{:<12}resource: {}".format("", permission_pair.resource))
                echo_fn()
            echo_fn()


class RoutesCSVPrinter(RoutesPrinter):
    """Routes CSV printer."""

    def echo(self, echo_fn: typing.Callable) -> None:
        """Print routes in csv format."""
        csv_output = StringIO()
        writer = DictWriter(csv_output, fieldnames=["methods", "path", "action", "resource"])
        writer.writeheader()

        for route in self.routes:
            header = True
            if len(route.permission_pairs) == 0:
                writer.writerow(
                    {
                        "methods": route.methods if header else "",
                        "path": route.path if header else "",
                        "action": "",
                        "resource": "",
                    },
                )
            else:
                for permission_pair in route.permission_pairs:
                    writer.writerow(
                        {
                            "methods": route.methods if header else "",
                            "path": route.path if header else "",
                            "action": permission_pair.action,
                            "resource": permission_pair.resource,
                        },
                    )
                    header = False

        csv_output.seek(0)
        echo_fn(csv_output.read())
