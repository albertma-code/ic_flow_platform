import os
import sys
import stat

os.environ['PYTHONUNBUFFERED'] = '1'
CWD = os.getcwd()

sys.path.append(str(CWD) + '/common')
import common


def gen_ifp_script(wrapper_script):
    """
    Generate wrapper script (shell) for python script.
    """
    print('>>> Generate wrapper script "' + str(wrapper_script) + '" ...')

    try:
        python_path = os.path.dirname(os.path.abspath(sys.executable))
        python_script = str(wrapper_script) + '.py'
        ld_library_path_setting = ''

        if 'LD_LIBRARY_PATH' in os.environ:
            ld_library_path_setting = 'export LD_LIBRARY_PATH=' + str(os.environ['LD_LIBRARY_PATH'])

        with open(wrapper_script, 'w') as TS:
            TS.write("""#!/bin/bash

# Set python3 path.
export PATH=""" + str(python_path) + """:$PATH

# Set install path.
export IFP_INSTALL_PATH=""" + str(CWD) + """

# Set LD_LIBRARY_PATH.
""" + str(ld_library_path_setting) + """

# Set writable Python/Matplotlib cache paths for read-only or network Python envs.
export PYTHONPYCACHEPREFIX="${PYTHONPYCACHEPREFIX:-/tmp/$USER/pycache}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-/tmp/$USER/mplconfig}"
mkdir -p "$PYTHONPYCACHEPREFIX" "$MPLCONFIGDIR"

# Execute ifp.py.
python3 \"$IFP_INSTALL_PATH/""" + str(python_script) + """\" \"$@\"
""")

        os.chmod(wrapper_script, stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
    except Exception as err:
        print('*Error*: Failed on generating top script "' + str(wrapper_script) + '": ' + str(err))
        sys.exit(1)


def gen_wrapper_scripts():
    gen_ifp_script('bin/ifp')


def gen_config_file():
    """
    Generate config file <IFP_INSTALL_PATH>/conf/config.py.
    """
    config_file = str(CWD) + '/config/config.py'

    print('')
    print('>>> Generate config file "' + str(config_file) + '".')

    if os.path.exists(config_file):
        print('*Warning*: config file "' + str(config_file) + '" already exists, will not update it.')
    else:
        try:
            with open(config_file, 'w') as CF:
                CF.writelines('## admin settings: Only administrator can modify below settings\n')
                for key, dic in common.config.admin_setting_dic.items():
                    value = dic['value']
                    note = dic['note']
                    CF.writelines('# ' + str(note) + '\n')

                    if isinstance(value, str):
                        value = '\"' + value + '\"'

                    CF.writelines(str(key) + ' = ' + str(value) + '\n\n')

                CF.writelines('## IFP Config settings: Users can define personal settings in ~/.ifp/config/config.py, Below are default value.\n')
                for key, dic in common.config.user_setting_dic.items():
                    value = dic['value']
                    note = dic['note']
                    CF.writelines('# ' + str(note) + '\n')
                    if isinstance(value, str):
                        value = '\"' + value + '\"'

                    CF.writelines(str(key) + ' = ' + str(value) + '\n\n')

            os.chmod(config_file, stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
        except Exception as error:
            print('*Error*: Failed on opening config file "' + str(config_file) + '" for write: ' + str(error))
            sys.exit(1)


def gen_top_sh_env():
    """
    Generate top environment file <IFP_INSTALL_PATH>/config/env.sh.
    """
    top_env_file = str(CWD) + '/config/env.sh'

    print('>>> Generate top sh environment file "' + str(top_env_file) + '" ...')

    try:
        with open(top_env_file, 'w') as TCF:
            TCF.write("""

#### Default EDA tool settings ####
# Set default TESSENT setting.

# Set default DC setting.

# Set default GENUS setting.

# Set default FORMALITY setting.

# Set default LEC setting.

# Set default PT setting.

# Set default TEMPUS setting.

# Set default ICC2 setting.

# Set default INNOVUS setting.

###################################

# Set default soffice path.


""")
    except Exception as err:
        print('*Error*: Failed on generating top environment file "' + str(top_env_file) + '": ' + str(err))
        sys.exit(1)


def gen_top_csh_env():
    """
    Generate top csh environment file <IFP_INSTALL_PATH>/config/env.csh.
    """
    top_env_file = str(CWD) + '/config/env.csh'

    print('>>> Generate top csh environment file "' + str(top_env_file) + '" ...')

    try:
        with open(top_env_file, 'w') as TCF:
            TCF.write("""

#### Default EDA tool settings ####
# Set default TESSENT setting.

# Set default DC setting.

# Set default GENUS setting.

# Set default FORMALITY setting.

# Set default LEC setting.

# Set default PT setting.

# Set default TEMPUS setting.

# Set default ICC2 setting.

# Set default INNOVUS setting.

###################################

# Set default soffice path.


""")
    except Exception as err:
        print('*Error*: Failed on generating top envionment file "' + str(top_env_file) + '": ' + str(err))
        sys.exit(1)


################
# Main Process #
################
def main():
    gen_wrapper_scripts()
    gen_config_file()
    gen_top_sh_env()
    gen_top_csh_env()

    print('')
    print('Install successfully!')


if __name__ == '__main__':
    main()
