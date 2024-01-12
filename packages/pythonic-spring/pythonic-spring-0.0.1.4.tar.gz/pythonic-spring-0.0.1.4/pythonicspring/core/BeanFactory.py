import json
import os
import pkgutil
from typing import Dict, List

from pythonicspring.configuration.ISpringConfig import ISpringConfig, EConfigType
from pythonicspring.configuration.bean_config.IBeanConfig import IBeanConfig
from pythonicspring.core.BeanProxy import BeanProxy
from pythonicspring.utils.GlobalInjector import global_injector
from pythonicspring.utils.GlobalScanner import get_annotated_bean
from pythonicspring.utils.TreeUtil import generate_tree


class BeanFactory:
    __instance__ = None
    __beans_dict__: Dict[str, BeanProxy] = {}
    __beans_config__: Dict[str, IBeanConfig] = {}

    def __init__(self, spring_app, scan_regex):
        if not spring_app or spring_app.__class__.__name__ != "SpringApplication":
            raise ValueError("Invalid BeanFactory initialize, Please use SpringApplication()")
        self.working_directory = os.path.dirname(os.getcwd())
        self._load_property_()
        with global_injector(__bean_factory__=self):
            self.add_beans_to_factory(scan_regex)

    def __new__(cls, *args, **kwargs):
        if not BeanFactory.__instance__:
            BeanFactory.__instance__ = object.__new__(cls)
        else:
            raise ValueError("Duplicated BeanFactory initialize")
        return BeanFactory.__instance__

    def add_beans_to_factory(self, scan_regex):
        scan_regex_dict = None if scan_regex is None else generate_tree(scan_regex)
        self.import_beans(scan_regex_dict)
        pass

    def import_beans(self, scan_regex_dict):
        classes = get_annotated_bean(self.working_directory, scan_regex_dict)
        for clazz in classes:
            if list(filter(lambda x: x['function_name'] in ['Service', 'pythonicspring.Service'], clazz['decorators'])):
                __import__(clazz['class_path'])

    def _load_property_(self):
        for relpath, dirs, files in os.walk(self.working_directory):
            if "spring.json" in files:
                try:
                    with open(os.path.join(relpath, "spring.json"), 'r') as load_f:
                        load_conf = ISpringConfig(**json.load(load_f))
                    if load_conf.config_type == EConfigType.bean:
                        self.__beans_config__.setdefault(load_conf.detail.id, load_conf.detail)
                except Exception as ex:
                    print(f'??? {ex}')

    def add_bean_to_factory(self, bean_name, bean_class=None) -> BeanProxy:
        prop_dict = {}
        bean_config = self.__beans_config__.get(bean_name)
        if bean_config is not None:
            prop_dict = zip(map(lambda x: x.name, bean_config.properties),
                            map(lambda x: x.value, bean_config.properties))
        if bean_class:
            instance = bean_class.__new__(bean_class)
            instance.__init__(**dict(prop_dict))
            if bean_name in self.__beans_dict__:
                self.__beans_dict__[bean_name].inject_bean(instance, bean_name)
            else:
                bean_proxy = BeanProxy(instance, bean_name)
                self.__beans_dict__[bean_name] = bean_proxy
        else:
            self.__beans_dict__[bean_name] = BeanProxy(None, bean_name)
        return self.__beans_dict__[bean_name]

    def get_bean_by_name(self, name: str) -> BeanProxy:
        return self.__beans_dict__.get(name)

    def get_beans_by_type(self, cls) -> List[BeanProxy]:
        return list(filter(lambda x: x.__class__.__name__ == cls, self.__beans_dict__.values()))
