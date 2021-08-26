from suspark.suspark_modules_factory import ModulesFactory
from suspark_modules.importsegy import ImportSegy
from suspark_modules.select_traces import SelectTraces
from suspark_modules.suagc import SUagc
from suspark_modules.sucdp import SUcdp
from suspark_modules.sufilter import SUfilter
from suspark_modules.suimp2d import SUimp2d
from suspark_modules.sunmo import SUnmo
from suspark_modules.susort import SUsort
from suspark_modules.sustack import SUstack


def register_test_modules(factory: ModulesFactory) -> None:
    factory.register_module_type("SUfilter", SUfilter)
    factory.register_module_type("SUsort", SUsort)
    factory.register_module_type("SUimp2d", SUimp2d)
    factory.register_module_type("SUstack", SUstack)
    factory.register_module_type("SUcdp", SUcdp)
    factory.register_module_type("SUnmo", SUnmo)
    factory.register_module_type("ImportSegy", ImportSegy)
    factory.register_module_type("SelectTraces", SelectTraces)
    factory.register_module_type("SUagc", SUagc)
