# sysls

A python command line tool that provides an alternative to `ls` when browsing a Linux sysfs.

It displays the contents of the sysfs files inline with filenames to get an easier overview of the state of a
directory.

## Installation

Available on pypi as `sysls`

## Usage

```shell-session
$ cd /sys/class/power_supply/BAT1
$ sysls
/device
/hwmon2
/power
/subsystem
/alarm............... 0
/capacity............ 92
/capacity_level...... Normal
/charge_full......... 3354000
/charge_full_design.. 3924000
/charge_now.......... 3106000
/current_now......... 0
/cycle_count......... 0
/manufacturer........ MSI
/model_name.......... BIF0_9
/present............. 1
/serial_number....... 
/status.............. Unknown
/technology.......... Li-ion
/type................ Battery
/voltage_min_design.. 10800000
/voltage_now......... 12023000
```

In case a file produces an error it will also be displayed inline:

```shell-session
$ sysls
/of_node
/power
/subsystem
/in_current0_label..... usbin_i
/in_current0_raw....... 235
/in_current0_scale..... 4604.492187500
/in_current1_label..... dcin_i
/in_current1_raw....... [-ENODATA]
```