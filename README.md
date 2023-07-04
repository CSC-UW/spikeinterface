# CSC-UW changes to vanilla SpikeInterface
We should aim to one day use the official SpikeInterface!

Detailed comparison: https://github.com/CSC-UW/spikeinterface/compare...wisc/dev

Summary, updated 5/11/2022:
- Explicitly sets MKL BLAS and LAPACK shared object libraries, which is necessary on Linux per [#199](https://github.com/MouseLand/Kilosort/issues/199#issuecomment-754971599).
  - Commits: [1](https://github.com/CSC-UW/spikeinterface/commit/1aae5e902c12e0560b54c1dc74fc43c238a3248e)
  - Perhaps we should submit a PR to spikeinterface / KiloSort install intstructions with info about how to obtain proper BLAS and LAPACK versions, then set the   relevant environment variables in `.bashrc`? Or is there a spikeinterface config file that users can add their BLAS and LAPACK locations to? Or can they be set as a keyword argument somewhere? Like in the Kilosort sorter class? 
- Allow passing amplitudes directly in compute_amplitude_cutoff (allow using Kilosort amplitudes)


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
