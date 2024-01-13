.. :orphan: is used below to try to remove the following warning: checking consistency... /home/econdami/Git_Projects/populse_mia/docs/source/installation/virtualisation_user_installation.rst: WARNING: document isn't included in any toctree

:orphan:

.. toctree::

+-----------------------+------------------------------------------------------+-------------------------------------+--------------------------------------------------+
|`Home <../index.html>`_|`Documentation <../documentation/documentation.html>`_|`Installation <./installation.html>`_|`GitHub <https://github.com/populse/populse_mia>`_|
+-----------------------+------------------------------------------------------+-------------------------------------+--------------------------------------------------+


Mia's user installation - Using virtualization
==============================================

The general installation process is to first, thanks to virtualization, make running BrainVisa on your system (see :ref:`prerequirements_1`).
Then, the installation will be almost identical to the one done directly on the host (see :ref:`installation_1`).

You can perform the installation by `following the detailed instruction provided by BrainVisa team <https://brainvisa.info/web/download.html>`_.
In this case, skip the :ref:`prerequirements_1` below and proceed directly to the :ref:`installation_1`.
Depending on the solution you have chosen, go to the Singularity container or the VirtualBox virtual machine and then follow the :ref:`installation_1` section below

You can also follow the full procedure below which uses Singularity virtualization technology.

.. _prerequirements_1:

Pre-requirements
----------------

* `For linux <./virtualisation_pre_req_linux.html>`_

* `For macos <./virtualisation_pre_req_macos.html>`_

* `For Windows 10 <./virtualisation_pre_req_windows10.html>`_

.. _installation_1:

Installation
------------

* If you followed `BrainVisa installation <https://brainvisa.info/web/download.html>`_ you should be in the container. Make sure to type the command ``bv bash`` if not.

* Then download the archive `here <https://github.com/populse/mia_install/archive/master.zip>`_.

* Unzip it and launch the following command in the extracted folder ("mia_install-main"): ::

	#update pip before installing mia
	python3 -m pip install --upgrade pip
        python3 install_mia.py

* If PyQt5 and pyyaml are not installed in your Python environment they will be first installed before launching the populse_mia's installation.

.. image:: ../images/mia_install_1.png
   :align: center
   :name: PyQt5 and pyyaml

|

* An error can sometimes occur, depending on your OS, after the installation of both packages, the Python environment not being correctly updated. If this error occurs launch the same command again to install populse_mia: ::

        python3 install_mia.py

|

* The Mia installation is now launched and you have to select four mandatory parameters:

  * Mia installation path: the folder where to install few directories and files necessary for the operation of populse_mia, set by default to ".populse_mia" in the current user's directory. Two folders will be created in the selected folder

    * populse_mia: containing Mia's configuration and resources files.

    * MRIFileManager: containing the file converter used in Mia.

    * MiaResources (external resources): containing resources needed to use populse_mia and mia_processes in some cases (references data as ROI, templates, ect...)


  * Mia projects path: the folder containing the analysis projects saved in Mia. A "projects" folder will be created in the selected folder.

  * Installation target: Check **Casa_distro** for installation on virtualized BrainVisa.

  * Operating mode: Choose between clinical and research mode (more information about `operating mode <../documentation/documentation.html#operating-mode>`_).

|

* If you already want to configure the use of Matlab and SPM (in license or standalone mode), you can also specify these several paths:

  * Matlab path:

    * Path of the Matlab executable file (is detected automatically).

      * e.g. for linux - macOS: /usr/local/MATLAB/R2018a/bin/matlab

      * e.g. for Windows 10: C:/Program Files/Matlab/R2019a/bin/matlab.exe

  * Matlab standalone path:

    * Path of the folder containing Matlab Compiler Runtine.

      * e.g. for linux - macOS: /usr/local/MATLAB/MATLAB_Runtime/v93/

      * e.g. for Windows 10: Nothing to declare here if you use spm standalone!

  * SPM path:

    * Path of the folder containing SPM12 code.

      * e.g. for linux - macOS: /usr/local/SPM/spm12

      * e.g. for Windows 10: C:/Program Files/Matlab/spm12

  * SPM standalone path:

    * Path to SPM12 standalone folder.

      * e.g. for linux - macOS: /usr/local/SPM/spm12_standalone (folder containing run_spm12.sh)

      * e.g. for Windows 10: C:/Program Files/Matlab/spm12_r7771/spm12 (with Windows 10, it is not necessary to declare the above Matlab standalone path in this case!)


.. image:: ../images/mia_install_2.png
   :align: center
   :name: Populse_MIA install widge

| You can install SPM and Matlab via `Third party software installations <./3rd-party_installations.html>`_ if those are not installed yet.

* Click on "Install" to install populse_mia with the selected parameters.

|

* The installation status is displayed. The last step (Python packages installation) may take a few minutes.

.. image:: ../images/mia_install_3.png
   :align: center
   :name: Populse_MIA install widget status

|

* When the packages have been installed, a summary of the installation is displayed.

.. image:: ../images/mia_install_4.png
   :align: center
   :name: Populse_MIA install widget summary

|

* To launch populse_mia: ::

        python3 -m populse_mia

|

* Set `populse_mia preferences <../documentation/preferences.html>`_

|

* You can also download the following folders:

      * `miadatausers <https://gricad-gitlab.univ-grenoble-alpes.fr/condamie/miadatausers>`_ : it contains initial user data for using / testing Mia
