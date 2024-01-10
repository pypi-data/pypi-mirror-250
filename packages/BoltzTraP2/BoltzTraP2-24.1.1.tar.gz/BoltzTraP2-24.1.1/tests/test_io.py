#    BoltzTraP2, a program for interpolating band structures and calculating
#                semi-classical transport coefficients.
#    Copyright (C) 2017-2024 Georg K. H. Madsen <georg.madsen@tuwien.ac.at>
#    Copyright (C) 2017-2024 Jesús Carrete <jesus.carrete.montana@tuwien.ac.at>
#    Copyright (C) 2017-2024 Matthieu J. Verstraete <matthieu.verstraete@ulg.ac.be>
#    Copyright (C) 2018-2019 Genadi Naydenov <gan503@york.ac.uk>
#    Copyright (C) 2020 Gavin Woolman <gwoolma2@staffmail.ed.ac.uk>
#    Copyright (C) 2020 Roman Kempt <roman.kempt@tu-dresden.de>
#    Copyright (C) 2022 Robert Stanton <stantor@clarkson.edu>
#
#    This file is part of BoltzTraP2.
#
#    BoltzTraP2 is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    BoltzTraP2 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with BoltzTraP2.  If not, see <http://www.gnu.org/licenses/>.

# Test the input and output capabilities of BoltzTraP2

import os
import os.path
import xml.etree.ElementTree as etree

import ase
import ase.io
import ase.io.wien2k
import netCDF4 as nc
import numpy as np
import pytest

import BoltzTraP2
import BoltzTraP2.io
import BoltzTraP2.units

mydir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(os.path.dirname(mydir), "data")


def test_parse_empty_xml_array():
    """_parse_xml_array should parse the empty array."""
    assert BoltzTraP2.io._parse_xml_array("") == []


def test_parse_xml_array():
    """_parse_xml_array should parse a non-empty array."""
    a = "1 1.2 1.3e-4 0.9e-5"
    ref = np.array([1.0, 1.2, 1.3e-4, 0.9e-5])
    assert np.allclose(BoltzTraP2.io._parse_xml_array(a), ref)


@pytest.fixture()
def si_vasprunxml():
    """Create an xml tree from a vasprun.xml for Si."""
    filename = os.path.join(datadir, "Si.vasp", "vasprun.xml")
    return etree.parse(filename)


@pytest.fixture()
def si_interpolated_vasprunxml():
    """Create an xml tree from a vasprun.xml for Si including interpolation."""
    filename = os.path.join(datadir, "Si.vasp.interp", "vasprun.xml")
    return etree.parse(filename)


def test_parse_vasp_name(si_vasprunxml):
    """_parse_vasp_name should return "unknown system" for Si."""
    assert BoltzTraP2.io._parse_vasp_name(si_vasprunxml) == "unknown system"


def test_parse_vasp_magmom():
    """_parse_vasp_magmom should work for unpolarized, collinear and
    noncollinear spins.
    """
    # Si, unpolarized
    xml = etree.parse(os.path.join(datadir, "Si.vasp", "vasprun.xml"))
    assert BoltzTraP2.io._parse_vasp_magmom(xml) is None
    # PbTe, unpolarized
    xml = etree.parse(
        os.path.join(datadir, "PbTe.vasp.unpolarized", "vasprun.xml")
    )
    assert BoltzTraP2.io._parse_vasp_magmom(xml) is None
    # PbTe, nocollinear
    xml = etree.parse(os.path.join(datadir, "PbTe.vasp.sl", "vasprun.xml"))
    magmom = BoltzTraP2.io._parse_vasp_magmom(xml)
    assert magmom.shape == (2, 3)
    assert np.allclose(magmom, np.ones_like(magmom))
    # LiZnSb, collinear
    xml = etree.parse(os.path.join(datadir, "LiZnSb.vasp", "vasprun.xml"))
    magmom = BoltzTraP2.io._parse_vasp_magmom(xml)
    assert magmom.shape == (6,)
    assert np.allclose(magmom, np.ones_like(magmom))


def test_parse_vasp_fermi(si_vasprunxml):
    """_parse_vasp_fermi should return the Fermi level of Si."""
    assert np.allclose(
        BoltzTraP2.io._parse_vasp_fermi(si_vasprunxml), 5.71756438
    )


def test_parse_vasp_kinter(si_vasprunxml, si_interpolated_vasprunxml):
    """_parse_vasp_kinter should discriminate between interpolated and
    non-interpolated VASP calculations.
    """
    assert BoltzTraP2.io._parse_vasp_kinter(si_vasprunxml) == 0
    assert BoltzTraP2.io._parse_vasp_kinter(si_interpolated_vasprunxml) == 3


def test_parse_vasp_lvel():
    """_parse_vasp_lvel should discriminate between VASP calculations with
    and without group velocities.
    """
    xml = etree.parse(os.path.join(datadir, "Si.vasp", "vasprun.xml"))
    assert BoltzTraP2.io._parse_vasp_lvel(xml)
    xml = etree.parse(os.path.join(datadir, "Si.vasp.noder", "vasprun.xml"))
    assert not BoltzTraP2.io._parse_vasp_lvel(xml)


def test_detect_vasp_broken_interpolation():
    """_detect_vasp_broken_interpolation should return True only for the
    Si.vasp.noder.interp.old directory.
    """
    directories = (
        "Si.vasp",
        "Si.vasp.noder",
        "Si.vasp.interp",
        "Si.vasp.noder.interp",
        "Si.vasp.interp.old",
    )
    for d in directories:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert not BoltzTraP2.io._detect_vasp_broken_interpolation(xml)
    xml = etree.parse(
        os.path.join(datadir, "Si.vasp.noder.interp.old", "vasprun.xml")
    )
    assert BoltzTraP2.io._detect_vasp_broken_interpolation(xml)


def test_detect_vasp_interpolated_velocities():
    """_detect_vasp_interpolated_velocities should return True only for the
    'interp' data directories.
    """
    directories = (
        "Si.vasp",
        "Si.vasp.noder",
        "Si.vasp.noder.interp",
        "Si.vasp.noder.interp.old",
    )
    for d in directories:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert not BoltzTraP2.io._detect_vasp_interpolated_velocities(xml)
    directories = ("Si.vasp.interp", "Si.vasp.interp.old")
    for d in directories:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert BoltzTraP2.io._detect_vasp_interpolated_velocities(xml)


def test_get_vasp_kpoints_path():
    """_get_vasp_kpoints_path should be able to detect all the different
    datasets containing lists of k points.
    """
    reference = {
        "Si.vasp": './kpoints/varray[@name="kpointlist"]',
        "Si.vasp.noder": './kpoints/varray[@name="kpointlist"]',
        "Si.vasp.interp": './calculation/eigenvelocities[@comment="interpolated"]/'
        'kpoints/varray[@name="kpointlist"]',
        "Si.vasp.noder.interp": './calculation/eigenvalues[@comment="interpolated"]/'
        'kpoints/varray[@name="kpointlist"]',
        "Si.vasp.interp.old": './calculation/eigenvalues[@comment="interpolated_ibz"]'
        '/electronvelocities/kpoints/varray[@name="kpointlist"]',
    }
    for d in reference:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert BoltzTraP2.io._get_vasp_kpoints_path(xml) == reference[d]


def test_get_vasp_energies_path():
    """_get_vasp_energies_path should be able to detect all the different
    datasets containing lists of energies.
    """
    reference = {
        "Si.vasp": "./calculation/eigenvalues/array/set",
        "Si.vasp.noder": "./calculation/eigenvalues/array/set",
        "Si.vasp.interp": './calculation/eigenvelocities[@comment="interpolated"]/'
        "eigenvalues/array/set",
        "Si.vasp.noder.interp": './calculation/eigenvalues[@comment="interpolated"]/'
        "eigenvalues/array/set",
        "Si.vasp.interp.old": './calculation/eigenvalues[@comment="interpolated_ibz"]'
        "/electronvelocities/eigenvalues/array/set",
    }
    for d in reference:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert BoltzTraP2.io._get_vasp_energies_path(xml) == reference[d]


def test_get_vasp_velocities_path():
    """_get_vasp_energies_path should be able to detect all the different
    datasets containing lists of velocities, or None if the calculation was
    performed with LVEL = F.
    """
    reference = {
        "Si.vasp": "./calculation/electronvelocities",
        "Si.vasp.interp": "./calculation/eigenvelocities",
        "Si.vasp.interp.old": './calculation/eigenvalues[@comment="interpolated_ibz"]'
        "/electronvelocities",
    }
    for d in reference:
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert BoltzTraP2.io._get_vasp_velocities_path(xml) == reference[d]
    for d in ("Si.vasp.noder", "Si.vasp.noder.interp"):
        xml = etree.parse(os.path.join(datadir, d, "vasprun.xml"))
        assert BoltzTraP2.io._get_vasp_velocities_path(xml) is None


def test_parse_vasp_structure(si_vasprunxml):
    """_parse_vasp_structure should be able to parse a Si structure."""
    atoms = BoltzTraP2.io._parse_vasp_structure(si_vasprunxml)
    # Test the lattice vectors
    ref = 5.467112115767304 * 0.5 * (np.ones((3, 3)) - np.eye(3))
    cell = atoms.get_cell()
    assert np.allclose(cell, ref)
    # Test the atomic positions
    ref = np.array([[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]])
    positions = atoms.get_scaled_positions()
    assert np.allclose(positions, ref)


def test_parse_vasp_ikpoints(si_vasprunxml):
    """_parse_vasp_ikpoints should return the right k points for Si."""
    kpoints = BoltzTraP2.io._parse_vasp_ikpoints(si_vasprunxml)
    assert kpoints.shape[0] == 165
    ref = np.load(os.path.join(mydir, "kpoints.npz"))["kpoints"]
    assert np.allclose(kpoints, ref)


def test_parse_vasp_eigenvalues(si_vasprunxml):
    """_parse_vasp_eigenvalues should return the right eigenvalues for Si."""
    eigenvalues = BoltzTraP2.io._parse_vasp_eigenvalues(si_vasprunxml)
    assert eigenvalues.shape == (1, 165, 8)
    # Only a few eigenvalues are actually checking
    assert np.allclose(
        eigenvalues[0, 0, :],
        [-6.1962, 5.6258, 5.6258, 5.6258, 8.1852, 8.1852, 8.1852, 8.7682],
    )
    assert np.allclose(
        eigenvalues[0, 20, :],
        [-4.9483, 0.6728, 4.1974, 4.8106, 7.6709, 9.0903, 9.2898, 12.7089],
    )
    assert np.allclose(
        eigenvalues[0, 163, :],
        [-2.1917, -1.7788, 1.6992, 2.1858, 8.7442, 9.6465, 11.3190, 11.4235],
    )


def test_parse_vasp_velocities(si_vasprunxml):
    """_parse_vasp_velocities should return the right velocities for Si."""
    kpoints, velocities = BoltzTraP2.io._parse_vasp_velocities(si_vasprunxml)
    assert kpoints.shape == (4913, 3)
    assert velocities.shape == (1, 4913, 8, 3)
    assert np.allclose(velocities[0, 0, :, :], np.zeros((8, 3)))
    assert np.allclose(
        velocities[0, 291, :, :],
        [
            [-0.4357, 1.3151, 0.4357],
            [4.3318, -5.7890, -4.3317],
            [0.0043, -3.6174, -0.0041],
            [-0.8963, -3.5206, 0.8961],
            [-1.9016, -2.4715, 1.9016],
            [2.4795, 4.1444, -2.4795],
            [-0.0996, 5.1275, 0.0996],
            [-3.7841, 5.4531, 3.7841],
        ],
    )
    assert np.allclose(
        velocities[0, 1075, :, :],
        [
            [-1.1381, 3.7815, -0.3560],
            [2.3511, -2.6098, 2.5102],
            [0.0351, -5.1461, -2.1357],
            [-0.2462, -2.2663, -2.5013],
            [-5.2723, -2.0726, 2.0552],
            [8.8141, 5.6665, -0.5984],
            [-9.1441, -2.1866, -8.3536],
            [0.1183, 6.8992, 8.3927],
        ],
    )


def test_parse_vasprunxml_notfound():
    """parse_vasprunxml should raise a FileNotFoundError if it cannot open the
    file.
    """
    with pytest.raises(FileNotFoundError):
        BoltzTraP2.io.parse_vasprunxml(os.path.join(datadir, "not_there.xml"))


def test_parse_vasprunxml_broken():
    """parse_vasprunxml should raise a ValueError for the old interpolated
    results without derivatives, which are known to be incorrect.
    """
    with pytest.raises(ValueError):
        BoltzTraP2.io.parse_vasprunxml(
            os.path.join(datadir, "Si.vasp.noder.interp.old", "vasprun.xml")
        )


def test_parse_vasprunxml():
    """parse_vasprunxml should be able to load the vasprun.xml for Si."""
    filename = os.path.join(datadir, "Si.vasp", "vasprun.xml")
    results = BoltzTraP2.io.parse_vasprunxml(filename)
    keys = tuple(sorted(list(results.keys())))
    # Check that all relevant information is in the results and that there are
    # no unknown pieces.
    assert keys == (
        "E",
        "atoms",
        "fermi",
        "kpoints",
        "magmom",
        "name",
        "nelect",
        "v",
    )
    assert results["E"].shape == (1, 165, 8)
    assert results["v"].shape == (1, 165, 8, 3)


@pytest.fixture()
def gsrfile():
    """Load the netCDF file for Si."""
    filename = os.path.join(datadir, "Si.abinit", "outsi_DS1_GSR.nc")
    ncf = nc.Dataset(filename, mode="r")
    return ncf


def test_parse_abinit_structure(gsrfile):
    """_parse_abinit_structure should be able to parse a Si structure."""
    atoms = BoltzTraP2.io._parse_abinit_structure(gsrfile)
    # Test the lattice vectors
    ref = (
        5.16731481286141
        * (np.ones((3, 3)) - np.eye(3))
        / BoltzTraP2.units.Angstrom
    )
    cell = atoms.get_cell()
    assert np.allclose(cell, ref)
    # Test the atomic positions
    ref = np.array([[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]])
    positions = atoms.get_scaled_positions()
    assert np.allclose(positions, ref)


def test_parse_abinitrun():
    """parse_abinitrun should be able to load the GSR.nc file for Si."""
    filename = os.path.join(datadir, "Si.abinit", "outsi_DS1_GSR.nc")
    results = BoltzTraP2.io.parse_abinitrun(filename)
    keys = tuple(sorted(list(results.keys())))
    # Check that all relevant information is in the results and that there are
    # no unknown pieces.
    assert keys == ("E", "atoms", "fermi", "kpoints", "name", "nelect")
    assert results["E"].shape == (1, 408, 10)


def test_W2Kmommat():
    """W2Kmommat should parse .mommat2 files correctly."""
    filename = os.path.join(datadir, "Si", "Si.struct")
    dum = ase.io.wien2k.read_struct(filename, ase=False)
    latt = dum[1]
    if latt == "R":
        latt = "P"
    conv = ase.io.wien2k.c2p(latt)
    filename = os.path.join(datadir, "Si", "Si.energy")
    kpoints = BoltzTraP2.io.W2Kene(filename, conv)[0]
    filename = os.path.join(datadir, "Si", "Si.mommat2")
    mommat, nemin, nemax = BoltzTraP2.io.W2Kmommat(filename, kpoints)
    assert nemin == 1
    assert nemax == 6
    ref = np.load(os.path.join(mydir, "Si_mommat_ref.npz"))["mommat"]
    assert np.allclose(mommat, ref)


def test_W2Kfermi():
    """W2Kfermi should return the right value of the Fermi level."""
    filename = os.path.join(datadir, "Si", "Si.scf")
    assert BoltzTraP2.io.W2Kfermi(filename) == 0.5 * 0.3766817831


def test_read_GENE_struct():
    """read_GENE_struct() should build the right Atoms object."""
    # Li: single-atom system
    filename = os.path.join(datadir, "Li", "Li_BLZTRP.structure")
    atoms = BoltzTraP2.io.read_GENE_struct(filename)
    ref = (
        0.3192047850e01
        * (np.ones((3, 3)) - 2.0 * np.eye(3))
        / BoltzTraP2.units.Angstrom
    )
    cell = atoms.get_cell()
    assert np.allclose(ref, cell)
    assert atoms.get_chemical_symbols() == ["Li"]
    ref = np.zeros(3)
    assert np.allclose(ref, atoms.get_positions())
    # LZS: multi-atom system
    filename = os.path.join(datadir, "LiZnSb.GENE", "LiZnSb.structure")
    atoms = BoltzTraP2.io.read_GENE_struct(filename)
    ref = (
        np.array(
            [
                [4.4309997546822144, 0.0000000000000000, 0.0000000000000000],
                [-2.2154998773411063, 3.8373583517174135, 0.0000000000000000],
                [0.0000000000000004, 0.0000000000000008, 7.1570000621175227],
            ]
        )
        / BoltzTraP2.units.Angstrom
    )
    cell = atoms.get_cell()
    assert np.allclose(ref, cell)
    assert atoms.get_chemical_symbols() == ["Sb", "Sb", "Zn", "Zn", "Li", "Li"]
    ref = (
        np.array(
            [
                [2.2154998994961068, 1.2791194377812773, 6.3339450549740075],
                [-0.0000000221549981, 2.5582389139361372, 2.7554450239152461],
                [2.2154998994961064, 1.2791194377812771, 3.5785000310587614],
                [-0.0000000221549983, 2.5582389139361368, 0.0000000000000000],
                [0.0000000000000003, 0.0000000000000005, 4.9812720432337958],
                [0.0000000000000001, 0.0000000000000001, 1.4027720121750344],
            ]
        )
        / BoltzTraP2.units.Angstrom
    )
    assert np.allclose(ref, atoms.get_positions())


def test_read_GENE_eneandmat_old():
    """read_GENE_eneandmat() should parse an old-style file correctly."""
    # This old-style file contains only one spin channel, and no momentum
    # matrix elements.
    filename = os.path.join(datadir, "Li", "Li_BLZTRP.energy")
    r = BoltzTraP2.io.read_GENE_eneandmat(filename)
    assert np.allclose(r[0], 0.6940745476e-01 / 2.0)
    assert r[1] == 2.0
    assert r[2].shape == (413, 3)
    assert np.allclose(r[2][0], [0.0, 0.0, 0.0])
    assert np.allclose(
        r[2][20], [0.3333333333e00, 0.4166666667e-01, 0.0000000000e00]
    )
    assert np.allclose(
        r[2][80], [0.3750000000e00, 0.8333333333e-01, 0.4166666667e-01]
    )
    assert np.allclose(
        r[2][391], [-0.4166666667e00, 0.4166666667e00, 0.3333333333e00]
    )
    assert r[3].shape == (3, 413)
    assert np.allclose(
        r[3][:, 20],
        np.array([-0.1963709022e-01, 0.5029658971e00, 0.8701510047e00]) / 2.0,
    )
    assert r[4] is None


def test_read_GENE_eneandmat_new():
    """read_GENE_eneandmat() should parse a new-style file correctly."""
    # This new-style file contains two spin channels as well as electronic
    # group velocities.
    filename = os.path.join(datadir, "Li.GENE.fromvasp", "Li.energy")
    r = BoltzTraP2.io.read_GENE_eneandmat(filename)
    assert np.allclose(r[0], 0.024951731946)
    assert r[1] == 1.0
    assert r[2].shape == (286, 3)
    assert np.allclose(r[2][0], [0.0, 0.0, 0.0])
    assert np.allclose(r[2][205], [-0.38095238, 0.47619048, 0.14285714])
    assert r[3].shape == (12, 286)
    assert np.allclose(
        r[3][:, 205],
        [
            -1.68363713,
            0.04813426,
            0.18563185,
            0.30062416,
            0.47661299,
            0.55504707,
            -1.68383558,
            0.047572,
            0.18507326,
            0.30008762,
            0.47603602,
            0.55446643,
        ],
    )
    assert r[4].shape == (286, 12, 3)
    assert np.allclose(
        r[4][205, :, :],
        np.array(
            [
                [3.32542058e-04, 8.16769966e-05, -1.55575232e-05],
                [1.16308043e-01, -2.65839177e-02, 2.03122912e-02],
                [-8.43431672e-02, 1.19983508e-01, -1.81672977e-02],
                [-8.65017735e-02, -4.95137622e-02, -8.76724771e-02],
                [-1.47465873e-02, 1.28310672e-02, 8.57472336e-02],
                [-4.77188129e-02, -1.68221553e-01, 1.73855321e-03],
                [3.34486748e-04, 8.16769966e-05, -1.55575232e-05],
                [1.16298320e-01, -2.65780836e-02, 2.03103465e-02],
                [-8.43470565e-02, 1.19973785e-01, -1.81828552e-02],
                [-8.65153863e-02, -4.95254303e-02, -8.76452515e-02],
                [-1.47485320e-02, 1.28349566e-02, 8.57783487e-02],
                [-4.76663063e-02, -1.68244890e-01, 1.70160410e-03],
            ]
        ),
    )


@pytest.fixture
def si_ESPRESSO_xml():
    """Create an ElementTree from the ESPRESSO output for Si."""
    filename = os.path.join(datadir, "Si.ESPRESSO", "out", "silicon.xml")
    return etree.parse(filename)


@pytest.fixture
def nitinol_ESPRESSO_xml():
    """Create an ElementTree from the ESPRESSO output for nitinol."""
    filename = os.path.join(datadir, "nitinol.ESPRESSO", "out", "nitinol.xml")
    return etree.parse(filename)


@pytest.fixture
def collinear_Fe_ESPRESSO_xml():
    """Create an ElementTree from the ESPRESSO output for collinear Fe."""
    filename = os.path.join(datadir, "Fe.ESPRESSO.collinear", "out", "fe.xml")
    return etree.parse(filename)


@pytest.fixture
def CrI3_ESPRESSO_xml():
    """Create an ElementTree from the ESPRESSO output for an antiferromagnetic
    configuration of CrI3.
    """
    filename = os.path.join(
        datadir, "CrI3.ESPRESSO.antiferro", "out", "CrI3.xml"
    )
    return etree.parse(filename)


def test_parse_ESPRESSO_title(si_ESPRESSO_xml):
    """_parse_ESPRESSO_title should return an empty string for Si."""
    assert BoltzTraP2.io._parse_ESPRESSO_title(si_ESPRESSO_xml) == ""


def test_parse_ESPRESSO_rlattvec(si_ESPRESSO_xml, nitinol_ESPRESSO_xml):
    """_parse_ESPRESSO_rlattvec should return the internal representation of
    the reciprocal lattice vectors for Si and for nitinol.
    """
    assert np.allclose(
        BoltzTraP2.io._parse_ESPRESSO_rlattvec(si_ESPRESSO_xml),
        np.array([[-1.0, -1.0, 1.0], [1.0, 1.0, 1.0], [-1.0, 1.0, -1.0]]).T,
    )
    assert np.allclose(
        BoltzTraP2.io._parse_ESPRESSO_rlattvec(nitinol_ESPRESSO_xml),
        np.array(
            [
                [
                    1.000000000000000e0,
                    1.192387274397203e-1,
                    0.000000000000000e0,
                ],
                [
                    0.000000000000000e0,
                    6.266299490075392e-1,
                    0.000000000000000e0,
                ],
                [
                    0.000000000000000e0,
                    0.000000000000000e0,
                    7.000000000000001e-1,
                ],
            ]
        ).T,
    )


def test_parse_ESPRESSO_structure(
    si_ESPRESSO_xml, nitinol_ESPRESSO_xml, CrI3_ESPRESSO_xml
):
    """_parse_ESPRESSO_structure should return the right structure for Si,
    for nitinol and for CrI3.
    """
    atoms = BoltzTraP2.io._parse_ESPRESSO_structure(si_ESPRESSO_xml)
    lattvec = (
        10.2076
        / BoltzTraP2.units.Angstrom
        * 0.5
        * np.array([[-1.0, 0.0, 1.0], [0.0, 1.0, 1.0], [-1.0, 1.0, 0.0]])
    )
    assert np.allclose(lattvec, atoms.get_cell())
    assert atoms.get_chemical_formula() == "Si2"
    assert np.all(atoms.get_tags() == [0, 0])
    atoms = BoltzTraP2.io._parse_ESPRESSO_structure(nitinol_ESPRESSO_xml)
    cosAB = -0.1184
    lattvec = np.array(
        [
            [2.8, 0.0, 0.0],
            [4.5 * cosAB, 4.5 * np.sqrt(1.0 - cosAB * cosAB), 0.0],
            [0.0, 0.0, 4.0],
        ]
    )
    assert np.allclose(lattvec, atoms.get_cell())
    fractional_positions = np.array(
        [
            [0.9475, 0.8070, 0.25],
            [0.0525, 0.1930, 0.75],
            [0.5274, 0.2790, 0.25],
            [0.4726, 0.7210, 0.75],
        ]
    )
    assert np.allclose(fractional_positions, atoms.get_scaled_positions())
    assert atoms.get_chemical_formula() == "Ni2Ti2"
    assert np.all(atoms.get_tags() == [0, 0, 1, 1])
    atoms = BoltzTraP2.io._parse_ESPRESSO_structure(CrI3_ESPRESSO_xml)
    # Test only the "tags" of CrI3 to check whether the extended chemical
    # symbol syntax has been correctly translated.
    assert atoms.get_chemical_formula() == "Cr4I12"
    assert np.all(
        atoms.get_tags() == [0, 1, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    )


def test_parse_ESPRESSO_bands(nitinol_ESPRESSO_xml, collinear_Fe_ESPRESSO_xml):
    """_parse_ESPRESSO_bands should read the correct electronis structure for
    nitinol and for collinear Fe.
    """
    bands = BoltzTraP2.io._parse_ESPRESSO_bands(nitinol_ESPRESSO_xml)
    assert bands["magmom"] is None
    assert bands["kpoints"].shape == (117, 3)
    assert bands["fermi"] == 6.449077782360640e-1
    assert bands["E"].shape == (117, 1, 36)
    assert np.allclose(
        bands["E"][0, 0, :],
        np.array(
            [
                -3.167343376955131e0,
                -3.167157072356015e0,
                -1.714733253240566e0,
                -1.713512214114199e0,
                -1.712025933779282e0,
                -1.711488606064103e0,
                -1.709501181108928e0,
                -1.709348210534368e0,
                -1.440608840646781e0,
                -1.437980035244009e0,
                -5.736148526147091e-1,
                -5.734225562531876e-1,
                -5.641196244063432e-1,
                -5.629779727167634e-1,
                -5.583931305867999e-1,
                -5.572669413145257e-1,
                3.503807693090326e-1,
                4.739963476400789e-1,
                4.919465094978584e-1,
                4.951701955777193e-1,
                4.961446685983859e-1,
                5.433946149865985e-1,
                5.544873264657331e-1,
                5.582317445474376e-1,
                5.655098293138613e-1,
                5.771517990624865e-1,
                5.862046963006870e-1,
                5.974301811969402e-1,
                6.287950586182175e-1,
                6.579332099870745e-1,
                6.644817866934270e-1,
                6.650996579881669e-1,
                6.935761636602082e-1,
                7.365888100183650e-1,
                7.485268248703090e-1,
                7.491846991830072e-1,
            ]
        ),
    )
    bands = BoltzTraP2.io._parse_ESPRESSO_bands(collinear_Fe_ESPRESSO_xml)
    assert bands["kpoints"].shape == (47, 3)
    assert bands["fermi"] == 8.122616158501044e-1
    assert bands["E"].shape == (47, 2, 12)
    assert np.allclose(
        bands["E"][0, 0, :],
        np.array(
            [
                -2.436206297651854e0,
                -1.172175834893222e0,
                -1.172175834891408e0,
                -1.172175834890710e0,
                4.589647913936384e-1,
                7.117364694095647e-1,
                7.117364694095716e-1,
                7.117364694095796e-1,
                7.667523346881642e-1,
                7.667523346881657e-1,
                1.771722831665474e0,
                1.771722831666007e0,
            ]
        ),
    )


def test_unpack_ESPRESSO_element():
    """_unpack_ESPRESSO_element should understand extended chemical symbols
    that comply with the pw.x input specification."""
    # The function should complain when a name is too long.
    with pytest.raises(ValueError):
        BoltzTraP2.io._unpack_ESPRESSO_element("abcd")
    # Test that other obviously wrong names also fail to be parsed.
    for ESPRESSO_element in ("", "_a", "__", "-a", "a", "a_-", "a_", "a", "A"):
        with pytest.raises(ValueError):
            BoltzTraP2.io._unpack_ESPRESSO_element(ESPRESSO_element)
    # Plain vanilla elements for which the function should not do anything.
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N") == ("N", "")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("Cu") == ("Cu", "")
    # Test case insensitivity.
    assert BoltzTraP2.io._unpack_ESPRESSO_element("n") == ("N", "")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("cu") == ("Cu", "")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("CU") == ("Cu", "")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("cU") == ("Cu", "")
    # Add a suffix without any separator.
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N1") == ("N", "1")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("Nc") == ("N", "c")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("Cu1") == ("Cu", "1")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("Cua") == ("Cu", "a")
    # Test that long suffixes are not accepted.
    with pytest.raises(ValueError):
        BoltzTraP2.io._unpack_ESPRESSO_element("C22")
    # Add a suffix with either of the two valid separators.
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N-1") == ("N", "1")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N_1") == ("N", "1")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N-a") == ("N", "a")
    assert BoltzTraP2.io._unpack_ESPRESSO_element("N_a") == ("N", "a")
