# -*- coding: utf-8 -*-
# ---------------------------------------------
#       @Time    : 2020/8/3 5:25 下午
#       @Author  : cxy =.=
#       @File    : main.py
#       @Software: PyCharm
#       @Desc    :
# ---------------------------------------------
import os
import shutil
import stat
import sys
import fastproject
from django.template import Engine, Context


def make_writeable(filename):
    if not os.access(filename, os.W_OK):
        st = os.stat(filename)
        new_permissions = stat.S_IMODE(st.st_mode) | stat.S_IWUSR
        os.chmod(filename, new_permissions)


def execute(argv):
    command, project_name = argv[1], argv[2]
    print(f'command: {command}')
    print(f'project_name: {project_name}')
    base_name = 'project_name'

    top_dir = os.path.join(os.getcwd(), project_name)
    print(f"top_dir: {top_dir}")
    os.makedirs(top_dir)

    camel_case_value = '_'.join(x for x in project_name.split('-'))
    context = Context({
        base_name: project_name,
        'project_directory': top_dir,
        'camel_case_project_name': camel_case_value,
    }, autoescape=False)

    template_dir = os.path.join(fastproject.__path__[0], 'fastproject', 'project_template')
    prefix_length = len(template_dir) + 1
    for root, dirs, files in os.walk(template_dir):
        print(root, dirs, files)
        path_rest = root[prefix_length:]
        relative_dir = path_rest.replace(base_name, camel_case_value)
        if relative_dir:
            target_dir = os.path.join(top_dir, relative_dir)
            os.makedirs(target_dir, exist_ok=True)

        for dirname in dirs[:]:
            if dirname.startswith('.') or dirname == '__pycache__':
                dirs.remove(dirname)

        for filename in files:
            if filename.endswith(('.pyo', '.pyc', '.py.class')):
                continue
            old_path = os.path.join(root, filename)
            new_path = os.path.join(
                top_dir, relative_dir, filename.replace(base_name, project_name)
            )
            for old_suffix, new_suffix in [('.py-tpl', '.py')]:
                if new_path.endswith(old_suffix):
                    new_path = new_path[:-len(old_suffix)] + new_suffix
                    break  # Only rewrite once

            # if os.path.exists(new_path):
            #     raise CommandError(
            #         "%s already exists. Overlaying %s %s into an existing "
            #         "directory won't replace conflicting files." % (
            #             new_path, self.a_or_an, app_or_project,
            #         )
            #     )

            # Only render the Python files, as we don't want to
            # accidentally render Django templates files
            if new_path.endswith('.py') or filename in []:
                with open(old_path, encoding='utf-8') as template_file:
                    content = template_file.read()
                template = Engine().from_string(content)
                content = template.render(context)
                with open(new_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(content)
            else:
                shutil.copyfile(old_path, new_path)

            try:
                shutil.copymode(old_path, new_path)
                make_writeable(new_path)
            except OSError:
                # self.stderr.write(
                #     "Notice: Couldn't set permission bits on %s. You're "
                #     "probably using an uncommon filesystem setup. No "
                #     "problem." % new_path, self.style.NOTICE)
                pass


def main():
    execute(sys.argv)


if __name__ == '__main__':
    main()
