# CSC-UW changes to vanilla SpikeInterface
Updated 5/9/2022

- Allows concatenation of datasets with different sample rates. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/4af9fe5566b3145678982d5cbfb8d8f28ddc7139), [2](https://github.com/CSC-UW/spikeinterface/commit/0ecc2cab58195167a1799c97b1cd55deffa7ff48)
  - Why do we need this? Can you add the explanation here, Tom? 
- Attempts to handle cases where user does not have permission to `chmod +x`? 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/26cca16f9310ffc3e93c073fe64005779f2b3c09)
  - Is this because `+x` needs to be set on `run_kilosort.sh`? 
  - Should this be dealt with in SI, or this really a sysadmin issue? If the former, can we submit as a PR? 
- Explicitly sets MKL BLAS and LAPACK shared object libraries, which is necessary on Linux per [#199](https://github.com/MouseLand/Kilosort/issues/199#issuecomment-754971599).
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/1aae5e902c12e0560b54c1dc74fc43c238a3248e)
  - Perhaps we should submit a PR to spikeinterface / KiloSort install intstructions with info about how to obtain proper BLAS and LAPACK versions, then set the   relevant environment variables in `.bashrc`? Or is there a spikeinterface config file that users can add their BLAS and LAPACK locations to? Or can they be set as a keyword argument somewhere? Like in the Kilosort sorter class? 
- Save diagnositc drift plots by default
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/66ddafa08b5f3f13b301c2ce2d5772d843af7cec)
  - Does Kilosort automatically save plots if this `plotDir` option is specified? Here we edit the `kilosort2_5_master.m`, but does this only work because our CSC-UW/Kilosort fork has corresponding changes that check for this `plotDir` option? If so, is there a way that only one repository (Kilosort or SpikeInterface) can be home to all the commits needed for this functionality? Otherwise we will never be able to get rid of one fork as long as the other exists.
- Allow specification of lambda parameter value from within SpikeInterface
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/10dc6a0ded76b750ed5e546625a4bdcb07a0257d)
  - This seems like it would be widely useful as a PR. 
- On UNIX, explicitly set the MATLAB shell to bash. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/832d00fd6fa4ffb6da89d10dad91d3e8bb7144fa)
  - Do we need to do this to prevent MATLAB from using Fish? Because Fish is not POSIX-compliant? If so, would this be widely useful as PR? 

It would be great if we could just use the official SpikeInterface!

# SpikeInterface: a unified framework for spike sorting

<table>
<tr>
  <td>Latest Release</td>
  <td>
    <a href="https://pypi.org/project/spikeinterface/">
    <img src="https://img.shields.io/pypi/v/spikeinterface.svg" alt="latest release" />
    </a>
  </td>
</tr>
<tr>
  <td>Documentation</td>
  <td>
    <a href="https://spikeinterface.readthedocs.io/">
    <img src="https://readthedocs.org/projects/spikeinterface/badge/?version=latest" alt="latest documentation" />
    </a>
  </td>
</tr>
<tr>
  <td>License</td>
  <td>
    <a href="https://github.com/SpikeInterface/spikeinterface/blob/master/LICENSE">
    <img src="https://img.shields.io/pypi/l/spikeinterface.svg" alt="license" />
    </a>
</td>
</tr>
<tr>
  <td>Build Status</td>
  <td>
    <a href="https://travis-ci.org/SpikeInterface/spikeinterface">
    <img src="https://travis-ci.org/SpikeInterface/spikeinterface.svg?branch=master" alt="travis build status" />
    </a>
  </td>
</tr>
<tr>
	<td>Gitter</td>
	<td>
		<a href="https://gitter.im/SpikeInterface/community">
		<img src="https://badges.gitter.im/SpikeInterface.svg" />
	</a>
	</td>
</tr>
</table>

SpikeInterface is a Python framework designed to unify preexisting spike sorting technologies into a single code base.

With SpikeInterface, users can:

- read/write many extracellular file formats.
- pre-process extracellular recordings.
- run many popular, semi-automatic spike sorters (also in Docker/Singularity containers).
- post-process sorted datasets.
- compare and benchmark spike sorting outputs.
- compute quality metrics to validate and curate spike sorting outputs.
- visualize recordings and spike sorting outputs.
- export report and export toPhy
- offer a powerful Qt-based viewer in separate package `spikeinterface-gui <https://https://github.com/SpikeInterface/spikeinterface-gui>`_
- have some powerful sorting components to build your own sorter.



**Please have a look at the [eLife paper](https://elifesciences.org/articles/61834) that describes in detail this project**

You can also have a look at the [spikeinterface-gui](https://https://github.com/SpikeInterface/spikeinterface-gui).

## Documentation

All documentation for spikeinterface 0.93 can be found [here](https://spikeinterface.readthedocs.io/en/latest/).

Documentation of current API release 0.12.0 is [here](https://spikeinterface.readthedocs.io/en/stable/).



## How to install spikeinteface

You can install the new `spikeinterface` version with pip:

```bash
pip install spikeinterface
```

To get the latest updates, you can install `spikeinterface` from sources:

```bash
git clone https://github.com/SpikeInterface/spikeinterface.git
cd spikeinterface
python setup.py install (or develop)
cd ..
```

## Versions

`spikeinterface` version 0.90 > 0.93:

  * breaks backward compatibility with 0.10/0.11/0.12/0.13 series.
  * has been first released in July 2021 (0.90.0)
  * is not a meta-package anymore
  * it doesn't depend on spikeextractors/spiketoolkit/spikesorters/spikecomparison/spikewidgets anymore


To install the old `spikeinterface` API (version<0.90), you can use pip and point to the old version:

```bash
pip install spikeinterface==0.13
```

We strongly recommend using the new version.

## Citation

If you find SpikeInterface useful in your research, please cite:

```bibtex
@article{buccino2020spikeinterface,
  title={SpikeInterface, a unified framework for spike sorting},
  author={Buccino, Alessio Paolo and Hurwitz, Cole Lincoln and Garcia, Samuel and Magland, Jeremy and Siegle, Joshua H and Hurwitz, Roger and Hennig, Matthias H},
  journal={Elife},
  volume={9},
  pages={e61834},
  year={2020},
  publisher={eLife Sciences Publications Limited}
}
```
