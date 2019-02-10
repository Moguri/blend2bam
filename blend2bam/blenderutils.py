import subprocess


def run_blender(args):
    subprocess.check_call(['blender', '--background'] + args)


def run_blender_script(script, args):
    run_blender([
        '-P', script,
        '--',
    ] + args)
