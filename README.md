![Settle](logo/settle.png)

Settle your favorite packages on your fresh installed Linux distribution

Settle helps you to install your favourite packages on your fresh installed Linux
distribution.
Settle expects you to pass a simple [YAML]() file containing a list of your favourite
packages, which are automatically installed by it.
Therefore you only need to keep an updated list of your favourite packages in order to
quickly install them the next time you reinstall your distro.
It can also be helpful for sysadmins that need to perform Linux installations on several
machines by saving time on the post install process.

## How does it work

You need to have a `packages.yml` file with your favourite packages grouped inside
categories. It could look something like this:

```yaml
basic:
    - git
    - gnupg
    - neovim

graphics:
    - gimp
    - inkscape

system:
    - gnome-disk-utility
    - gnome-system-monitor
```

Then run Settle:

```bash
settle packages.yml
```

Now Settle will ask you if you want to refresh the packages lists, update all the
installed packages and then will ask you which packages you want to install:

![Settle example](settle_example.gif)


## How to install

Currently the only way to install it is cloning the GitHub repository:

```bash
git clone https://github.com/santisoler/settle
```

And then install it:
```bash
cd settle
pip install .
```

I plan to upload Settle to [Pypi]() in the future for make the installation easier.


## How to use

We need to write a `packages.yml` file containing the packages we will eventually want
to install in the future.
They can be grouped inside categories so we can specify what packages we want to install
each time we run Settle.
Settle will ask us to choose which categories want to be installed, so only the packages
inside the chosen categories will be installed.
Therefore we can include any package we eventually use on `packages.yml`, but choose
which packages we definitely want to install after a fresh Linux installation.

If we know that we will always install the packages on some specific categories, we can
define a `default` section where we can specify which categories will be checked-off by
default:

```yaml
default:
    - basic
    - system

basic:
    - git
    - gnupg
    - neovim

graphics:
    - gimp
    - inkscape

system:
    - gnome-disk-utility
    - gnome-system-monitor
```

## Related projects

- https://github.com/snwh/ubuntu-post-install
- https://github.com/Cyclenerd/postinstall
- https://github.com/ansible/ansible

## License

All content under [MIT License](), except where noted.

Settle logo is released under
[Licencia Creative Commons Atribución 4.0 Internacional](http://creativecommons.org/licenses/by/4.0/).
Settle logo has been created over an adapted version of the icon made by
[Smashicons](https://www.flaticon.com/authors/smashicons) from www.flaticon.com.
