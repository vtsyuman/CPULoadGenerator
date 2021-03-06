#!/usr/bin/python

# Authors: Gaetano Carlucci
#          Giuseppe Cofano
from .Monitor import MonitorThread
from .Controller import ControllerThread
from .ClosedLoopActuator import ClosedLoopActuator
from argparse import ArgumentParser
from multiprocessing import Process, cpu_count
from pyvirtualdisplay import Display


def worker(core_num, cpu_load, d, plot, reporter_dir=None):
    monitor = MonitorThread(core_num, 0.1)
    monitor.start()

    control = ControllerThread(0.1)
    control.start()
    control.CT = cpu_load
    actuator = ClosedLoopActuator(control, monitor, d, core_num, cpu_load, plot, reporter_dir)

    actuator.run()

    actuator.close()
    monitor.running = False
    control.running = False
    monitor.join()
    control.join()


def main(cores, cpu_load, duration, use_plot, reporter_dir=None):
    display = Display(visible=0, size=(800, 600))
    display.start()
    procs = []
    for core_num in cores:
        proc = Process(target=worker, args=(int(core_num), cpu_load, duration, use_plot, reporter_dir))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    display.stop()
    return True


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cores', nargs='+',  dest='cores', required=True)
    parser.add_argument('--cpu-load', type=float, dest='cpu_load')
    parser.add_argument('--plot', type=int, dest='plot')
    parser.add_argument('--duration', type=int, dest='duration')
    args = parser.parse_args()
    args.cores = [int(num) for num in args.cores]
    supported_cores = list(range(cpu_count()))
    for core in args.cores:
        if core not in supported_cores:
            raise EnvironmentError(
                'the selected core ({}) is not in the list of supported environments {}'.format(core, supported_cores))
    main(args.cores, args.cpu_load, args.duration, use_plot=args.plot)
