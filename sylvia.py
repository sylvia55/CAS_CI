import paramiko, subprocess, sys
import ConfigParser, os
from pexpect import *

def p4_login():
    run('p4 login', events={'Enter password':'@#$234wer\n'})

def get_parameter(section, param):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config.get(section,param)

config_file = 'config.ini'

def local_command(cmd):
    try:
        retcode = subprocess.call(cmd, shell=True)
        if retcode < 0:
            print >>sys.stderr, "cmd error", -retcode
        else:
            print >>sys.stderr, "child returned", retcode
    except OSError as e:
        print >>sys.stderr, "Execution failed:", e

        
#def sync_p4(param):
#    cmd = get_parameter('p4cmd', param)
#    local_command(cmd)


def dlp_template():
    os.chdir('/home/ciPolicy/Ent/SaaSSecurity/Dev/Office365-CAS/Linux/src/common/tools/generate_DLP_i18n/')
    os.system('sh build.sh')

def policy_build():
    os.chdir('/home/ciPolicy/Ent/SaaSSecurity/Dev/Office365-CAS/Linux/src/policy/Build/')
    os.system('sh build.sh 0001')

p4_login()
#sync_p4('policy')

#jdbc = get_parameter('p4cmd', 'jdbc')
#local_command(jdbc)

params1 = ['policy', 'policy', 'p4cmd', 'p4cmd', 'p4cmd', 'p4cmd', 'p4cmd']
params2 = ['stop_jetty', 'remove_policy', 'policy', 'jdbc', 'dlp_path', 'change_pwd', 'L10n']
for i in range(0, len(params1)):
    cmd = get_parameter(params1[i], params2[i])
    print cmd
    local_command(cmd)
#sync_p4('dlp_path')
#change_pwd = get_parameter('p4cmd', 'change_pwd')
#local_command(change_pwd)
#local_command(l10n)
dlp_template()
policy_build()
os.chdir('/home/ciPolicy/sylvia')
start_policy = get_parameter('p4cmd', 'start_policy')
local_command(start_policy)
