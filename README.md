# CSC-UW changes to vanilla SpikeInterface
We should aim to one day use the official SpikeInterface!

Detailed comparison: https://github.com/CSC-UW/spikeinterface/compare/master...wisc/dev

Summary, updated 5/11/2022:
- Temporary fix in append/concat_segments to allow sorting files with different srate
- Expose do_preprocessing Kilosrt2.5 option to SpikeInterface
  - Commits: 
  - Specific to custom csc-uw/kilosort branch 
- Explicitly sets MKL BLAS and LAPACK shared object libraries, which is necessary on Linux per [#199](https://github.com/MouseLand/Kilosort/issues/199#issuecomment-754971599).
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/1aae5e902c12e0560b54c1dc74fc43c238a3248e)
  - Perhaps we should submit a PR to spikeinterface / KiloSort install intstructions with info about how to obtain proper BLAS and LAPACK versions, then set the   relevant environment variables in `.bashrc`? Or is there a spikeinterface config file that users can add their BLAS and LAPACK locations to? Or can they be set as a keyword argument somewhere? Like in the Kilosort sorter class? 
- Expose lambda parameter to SpikeInterface
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/10dc6a0ded76b750ed5e546625a4bdcb07a0257d)
  - This seems like it would be widely useful as a PR. 

### Changes merged in vanilla Spikeinterface 
- On UNIX, explicitly set the MATLAB shell to bash. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/832d00fd6fa4ffb6da89d10dad91d3e8bb7144fa)
  - We need to do this to prevent MATLAB from using Fish. Otherwise [this](https://github.com/MouseLand/Kilosort/blob/74c64485d8dd0bc5dd976d7bf51a46873b08351f/utils/rezToPhy.m#L186) line fails with a `command not found` error. I (TB) don't understand why that is the case (and it doesn't happen when default shell is Zsh or Bash). I think this would be a useful PR but there might be a better way of adressing this, which applies to all sorters (it might even be an issue with Fish itself).
- Expose do_correction option to SpikeInterface
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/89b8c44112a81100029b7a54123ba44ee8f2b3fd)
  - This seems like it would be widely useful as a PR. 
- Allows concatenation of datasets with different sample rates. 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/4af9fe5566b3145678982d5cbfb8d8f28ddc7139), [2](https://github.com/CSC-UW/spikeinterface/commit/0ecc2cab58195167a1799c97b1cd55deffa7ff48)
  - I needed this at some point to concatenating datasets from different runs for sorting , because sampling_rate slightly changes across SpikeGLX runs. This change is currently NOT reflected in wisc_ecephys_tools (which should fail when trying to concatenate across runs). 

### Reverted changes
- Save diagnositc drift plots by default
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/66ddafa08b5f3f13b301c2ce2d5772d843af7cec)
  - Reversion: 
  - Vanilla Kilosort does not save any of the plots generated during drift correction when run from spikeinterface. 
  In our CSC-UW fork (branch wisc/2.5/dev) [it now does](https://github.com/CSC-UW/Kilosort/commit/a401d21f1feadd46591a085bcc390ab90d786ace) by default, at <output_dir>/plots_ks
- Attempts to handle cases where user does not have permission to `chmod +x`? 
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/26cca16f9310ffc3e93c073fe64005779f2b3c09)
  - Reversion: [1](https://github.com/CSC-UW/spikeinterface/commit/0b5987fcb58283352ccd6d7dc71cab4541f23cdf)

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
    <a href="https://github.com/SpikeInterface/spikeinterface/actions/workflows/full-test-with-codecov.yml/badge.svg">
    <img src="https://github.com/SpikeInterface/spikeinterface/actions/workflows/full-test-with-codecov.yml/badge.svg" alt="CI build status" />
    </a>
  </td>
</tr>
<tr>
	<td>Codecov</td>
	<td>
		<a href="https://codecov.io/github/spikeinterface/spikeinterface">
		<img src="https://codecov.io/gh/spikeinterface/spikeinterface/branch/master/graphs/badge.svg" alt="codecov" />
		</a>
	</td>
</tr>
</table>

[![Twitter](https://img.shields.io/badge/@spikeinterface-%231DA1F2.svg?style=for-the-badge&logo=Twitter&logoColor=white)](https://twitter.com/spikeinterface) [![Mastodon](https://img.shields.io/badge/-@spikeinterface-%232B90D9?style=for-the-badge&logo=mastodon&logoColor=white)](https://fosstodon.org/@spikeinterface)


SpikeInterface is a Python framework designed to unify preexisting spike sorting technologies into a single code base.

Please [Star](https://github.com/SpikeInterface/spikeinterface/stargazers) the project to support us and [Watch](https://github.com/SpikeInterface/spikeinterface/subscription) to always stay up-to-date!


With SpikeInterface, users can:

- read/write many extracellular file formats.
- pre-process extracellular recordings.
- run many popular, semi-automatic spike sorters (also in Docker/Singularity containers).
- post-process sorted datasets.
- compare and benchmark spike sorting outputs.
- compute quality metrics to validate and curate spike sorting outputs.
- visualize recordings and spike sorting outputs in several ways (matplotlib, sortingview, in jupyter)
- export report and export to phy
- offer a powerful Qt-based viewer in separate package [spikeinterface-gui](https://github.com/SpikeInterface/spikeinterface-gui)
- have some powerful sorting components to build your own sorter.


## Documentation

Detailed documentation for spikeinterface can be found [here](https://spikeinterface.readthedocs.io/en/latest).

Several tutorials to get started can be found in [spiketutorials](https://github.com/SpikeInterface/spiketutorials).

There are also some useful notebooks [on our blog](https://spikeinterface.github.io) that cover advanced benchmarking 
and sorting components.

You can also have a look at the [spikeinterface-gui](https://github.com/SpikeInterface/spikeinterface-gui).


## How to install spikeinteface

You can install the new `spikeinterface` version with pip:

```bash
pip install spikeinterface[full]
```

The `[full]` option installs all the extra dependencies for all the different sub-modules. 

To install all interactive widget backends, you can use:

```bash
 pip install spikeinterface[full,widgets]
```


To get the latest updates, you can install `spikeinterface` from sources:

```bash
git clone https://github.com/SpikeInterface/spikeinterface.git
cd spikeinterface
pip install -e .
cd ..
```


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
