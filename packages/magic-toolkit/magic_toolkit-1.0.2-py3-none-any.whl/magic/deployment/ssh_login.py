import subprocess
import os
from .remote_manager import RemoteDeviceManager
import magic
import yaml

def config_parser(sub_parsers):
    p = sub_parsers.add_parser("ssh", help="ssh helper, check remote devices")
    p.add_argument('argv', nargs="*", help='command args')
    p.add_argument('--password', default=None, help='password')
    p.add_argument('-p', '--port', type=int, default=22, help='port')
    p.add_argument('--config', help='rsync.yaml')
    p.set_defaults(func=execute)

def execute(args):
    argv = args.argv
    remote_manager = RemoteDeviceManager()
    # 参数解析
    if len(argv) == 0:
        config_file = args.config or os.path.join(os.getcwd(), '.vscode/rsync.yaml')
        if not os.path.exists(config_file):
            raise FileNotFoundError("Not found config '{}'".format(config_file))
        with open(config_file, 'r') as f:
            conf = yaml.safe_load(f)
        ssh_connect(conf['host'], conf.get('password'), conf.get('port', 22),
                    IdentityFile=conf.get("IdentityFile"))
    elif argv[0] == 'list':
        remote_manager.list_all_devices()
    elif argv[0] == 'info':
        device = remote_manager.get_device(argv[1])
        print(device)
    elif argv[0] == 'config':
        remote_config_file = os.path.join(magic.config_root, 'remote_device.pt')
        subprocess.run(f'gedit {remote_config_file}', shell=True)
    else:
        host, password, port, IdentityFile = argv[0], args.password, args.port, None
        device = remote_manager.get_device(argv[0])
        if device is not None:
            # search device by name, host
            host, password, port, IdentityFile = device.host, device.password, device.port, device.IdentityFile
        ssh_connect(host, password, port, IdentityFile=IdentityFile)

def ssh_connect(host, password=None, port=22, **kwargs):
    if kwargs.get('IdentityFile'):
        subprocess.run('ssh -p {} {} -i {}'.format(port, host, kwargs.get('IdentityFile')), shell=True)
    elif password:
        assert isinstance(password, str)
        sshpass_cmd = 'sshpass -p {} ssh -p {} -o StrictHostKeyChecking=no {}'.format(password, port, host)
        subprocess.run(sshpass_cmd, shell=True)
    else:
        subprocess.run('ssh -p {} {}'.format(port, host), shell=True)
