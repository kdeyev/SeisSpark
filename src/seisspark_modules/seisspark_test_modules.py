from seisspark.seisspark_modules_factory import ModulesFactory
from seisspark_modules.importsegy import ImportSegy
from seisspark_modules.select_traces import SelectTraces
from seisspark_modules.suagc import SUagc
from seisspark_modules.sucdp import SUcdp
from seisspark_modules.sufilter import SUfilter
from seisspark_modules.suimp2d import SUimp2d
from seisspark_modules.sunmo import SUnmo
from seisspark_modules.susort import SUsort
from seisspark_modules.sustack import SUstack


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
