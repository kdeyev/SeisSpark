from suspark.suspark_modules_factory import ModulesFactory
from suspark_modules.sufilter import SUfilter
from suspark_modules.suimp2d import SUimp2d
from suspark_modules.susort import SUsort


def register_test_modules(factory: ModulesFactory) -> None:
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUsort", SUsort)
    factory.register_module_type("SUimp2d", SUimp2d)
