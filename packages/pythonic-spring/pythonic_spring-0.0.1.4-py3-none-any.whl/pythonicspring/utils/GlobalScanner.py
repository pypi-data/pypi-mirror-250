import os
import ast


def _get_methods_(cls_node):
    methods = []
    for node in ast.iter_child_nodes(cls_node):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)
    return methods


def _get_function_name_(func):
    if isinstance(func, ast.Name):
        return func.id
    elif isinstance(func, ast.Attribute):
        return f"{_get_function_name_(func.value)}.{func.attr}"


def _get_classes_(cls_node, path):
    classes = []
    for node in ast.iter_child_nodes(cls_node):
        if isinstance(node, ast.ClassDef):
            name = node.name
            class_path = f"{path}.{name}"
            decorators = []
            for decorator in node.decorator_list:
                keywords = None
                if isinstance(decorator, ast.Call):
                    function_name = _get_function_name_(decorator.func)
                    keywords = list(map(lambda x: {'arg': x.arg, 'value': x.value.value}, decorator.keywords))
                elif isinstance(decorator, ast.Name):
                    function_name = decorator.id
                decorators.append({'function_name': function_name, 'keywords': keywords})
            classes.append({'class_name': name, 'class_path': class_path, 'decorators': decorators})
    return classes

@staticmethod
def get_annotated_bean(dir_path, scan_regex_dict, base_paths=[]):
    results = []
    for file in os.listdir(dir_path):
        next_dict = scan_regex_dict
        if scan_regex_dict is not None and not scan_regex_dict.is_stella():
            next_dict = scan_regex_dict.get_child("*") or scan_regex_dict.get_child(file)
            if not next_dict:
                continue
        if file.endswith('.py'):
            file_path = os.path.join(dir_path, file)
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
            classes = _get_classes_(tree, '.'.join(base_paths))
            if classes:
                results.extend(classes)
        elif os.path.isdir(f"{dir_path}/{file}"):
            results.extend(get_annotated_bean(f"{dir_path}/{file}", next_dict, [*base_paths, file]))
        # for file in files:
        #     if file.endswith('.py'):
        #         file_path = os.path.join(root, file)
        #         with open(file_path, 'r') as f:
        #             tree = ast.parse(f.read())
        #         classes = _get_classes_(tree, '.'.join(base_paths))
        #         if classes:
        #             results.extend(classes)
    return results


if __name__ == '__main__':
    print(get_annotated_bean("D:\\Project\\python\\pythonic-spring\\test"))
    pass
