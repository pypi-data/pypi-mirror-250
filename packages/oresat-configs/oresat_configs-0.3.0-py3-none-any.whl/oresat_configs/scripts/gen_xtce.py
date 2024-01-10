"""Generate XTCE for the beacon."""

import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from datetime import datetime

import canopen

from .. import ORESAT_NICE_NAMES, OreSatConfig, OreSatId

GEN_XTCE = "generate beacon xtce file"
GEN_XTCE_PROG = "oresat-gen-xtce"

CANOPEN_TO_XTCE_DT = {
    canopen.objectdictionary.BOOLEAN: "bool",
    canopen.objectdictionary.INTEGER8: "int8",
    canopen.objectdictionary.INTEGER16: "int16",
    canopen.objectdictionary.INTEGER32: "int32",
    canopen.objectdictionary.INTEGER64: "int64",
    canopen.objectdictionary.UNSIGNED8: "uint8",
    canopen.objectdictionary.UNSIGNED16: "uint16",
    canopen.objectdictionary.UNSIGNED32: "uint32",
    canopen.objectdictionary.UNSIGNED64: "uint64",
    canopen.objectdictionary.VISIBLE_STRING: "string",
    canopen.objectdictionary.REAL32: "float",
    canopen.objectdictionary.REAL64: "double",
}

DT_LEN = {
    canopen.objectdictionary.BOOLEAN: 8,
    canopen.objectdictionary.INTEGER8: 8,
    canopen.objectdictionary.INTEGER16: 16,
    canopen.objectdictionary.INTEGER32: 32,
    canopen.objectdictionary.INTEGER64: 64,
    canopen.objectdictionary.UNSIGNED8: 8,
    canopen.objectdictionary.UNSIGNED16: 16,
    canopen.objectdictionary.UNSIGNED32: 32,
    canopen.objectdictionary.UNSIGNED64: 64,
    canopen.objectdictionary.VISIBLE_STRING: 0,
    canopen.objectdictionary.REAL32: 32,
    canopen.objectdictionary.REAL64: 64,
}


def make_obj_name(obj: canopen.objectdictionary.Variable) -> str:
    """get obj name."""

    name = ""
    if obj.index < 0x5000:
        name += "c3_"

    if isinstance(obj.parent, canopen.ObjectDictionary):
        name += obj.name
    else:
        name += f"{obj.parent.name}_{obj.name}"

    return name


def make_dt_name(obj) -> str:
    """Make xtce data type name."""

    type_name = CANOPEN_TO_XTCE_DT[obj.data_type]
    if obj.name in ["unix_time", "updater_status"]:
        type_name = obj.name
    elif obj.value_descriptions:
        if isinstance(obj.parent, canopen.ObjectDictionary):
            type_name += f"_c3_{obj.name}"
        else:
            type_name += f"_{obj.parent.name}_{obj.name}"
    elif obj.data_type == canopen.objectdictionary.VISIBLE_STRING:
        type_name += f"{len(obj.default) * 8}"
    elif obj.unit:
        type_name += f"_{obj.unit}"
    type_name = type_name.replace("/", "p").replace("%", "percent")

    type_name += "_type"

    return type_name


def write_xtce(config: OreSatConfig, dir_path: str = "."):
    """Write beacon configs to a xtce file."""

    root = ET.Element(
        "SpaceSystem",
        attrib={
            "name": ORESAT_NICE_NAMES[config.oresat_id],
            "xmlns:xtce": "http://www.omg.org/space/xtce",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": (
                "http://www.omg.org/spec/XTCE/20180204 "
                "https://www.omg.org/spec/XTCE/20180204/SpaceSystem.xsd"
            ),
        },
    )

    header = ET.SubElement(
        root,
        "Header",
        attrib={
            "validationStatus": "Working",
            "classification": "NotClassified",
            "version": f'{config.od_db["c3"]["beacon"]["revision"].value}.0',
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    )
    author_set = ET.SubElement(header, "AuthorSet")
    author = ET.SubElement(author_set, "Author")
    author.text = "PSAS (Portland State Aerospace Society)"

    tm_meta = ET.SubElement(root, "TelemetryMetaData")
    tm_meta_para = ET.SubElement(tm_meta, "ParameterTypeSet")

    para_type = ET.SubElement(
        tm_meta_para,
        "AbsoluteTimeParameterType",
        attrib={
            "name": "unix_time",
            "shortDescription": "Unix coarse timestamp",
        },
    )
    enc = ET.SubElement(para_type, "Encodings")
    ET.SubElement(
        enc,
        "IntegerDataEncoding",
        attrib={
            "byteOrder": "leastSignificantByteFirst",
            "sizeInBits": "32",
        },
    )
    ref_time = ET.SubElement(para_type, "ReferenceTime")
    epoch = ET.SubElement(ref_time, "Epoch")
    epoch.text = "1970-01-01T00:00:00.000"

    para_types = ["unix_time"]
    for obj in config.beacon_def:
        name = make_dt_name(obj)
        if name in para_types:
            continue
        para_types.append(name)

        if obj.data_type == canopen.objectdictionary.BOOLEAN:
            para_type = ET.SubElement(
                tm_meta_para,
                "BooleanParameterType",
                attrib={
                    "name": name,
                    "zeroStringValue": "0",
                    "oneStringValue": "1",
                },
            )
            unit_set = ET.SubElement(para_type, "UnitSet")
            dt_len = DT_LEN[obj.data_type] # Length of the data type
            # Integer-type encoding for enums
            int_dt_enc = ET.SubElement(
                para_type,
                "IntegerDataEncoding",
                attrib={
                    "sizeInBits": str(dt_len)
                }
            )
        elif obj.data_type in canopen.objectdictionary.UNSIGNED_TYPES and obj.value_descriptions:
            para_type = ET.SubElement(
                tm_meta_para,
                "EnumeratedParameterType",
                attrib={
                    "name": name,
                },
            )
            unit_set = ET.SubElement(para_type, "UnitSet")
            dt_len = DT_LEN[obj.data_type] # Length of the data type
            # Integer-type encoding for enums
            int_dt_enc = ET.SubElement(
                para_type,
                "IntegerDataEncoding",
                attrib={
                    "sizeInBits": str(dt_len)
                }
            )
            enum_list = ET.SubElement(para_type, "EnumerationList")
            for value, name in obj.value_descriptions.items():
                ET.SubElement(
                    enum_list,
                    "Enumeration",
                    attrib={
                        "value": str(value),
                        "label": name,
                    },
                )
        elif obj.data_type in canopen.objectdictionary.INTEGER_TYPES:
            if obj.data_type in canopen.objectdictionary.UNSIGNED_TYPES:
                signed = False
                encoding = "unsigned"
            else:
                signed = True
                encoding = "twosComplement"

            para_type = ET.SubElement(
                tm_meta_para,
                "IntegerParameterType",
                attrib={
                    "name": name,
                    "signed": str(signed).lower(),
                },
            )

            para_unit_set = ET.SubElement(para_type, "UnitSet")
            if obj.unit:
                para_unit = ET.SubElement(
                    para_unit_set,
                    "Unit",
                    attrib={
                        "description": obj.unit,
                    },
                )
                para_unit.text = obj.unit

            data_enc = ET.SubElement(
                para_type,
                "IntegerDataEncoding",
                attrib={
                    "byteOrder": "leastSignificantByteFirst",
                    "encoding": encoding,
                    "sizeInBits": str(DT_LEN[obj.data_type]),
                },
            )
            if obj.factor != 1:
                def_cal = ET.SubElement(data_enc, "DefaultCalibrator")
                poly_cal = ET.SubElement(def_cal, "PolynomialCalibrator")
                ET.SubElement(
                    poly_cal,
                    "Term",
                    attrib={
                        "exponent": "1",
                        "coefficient": str(obj.factor),
                    },
                )
        elif obj.data_type == canopen.objectdictionary.VISIBLE_STRING:
            para_type = ET.SubElement(
                tm_meta_para,
                "StringParameterType",
                attrib={
                    "name": name,
                },
            )
            str_para_type = ET.SubElement(
                para_type,
                "StringDataEncoding",
                attrib={
                    "encoding": "UTF-8",
                },
            )
            size_in_bits = ET.SubElement(str_para_type, "SizeInBits")
            fixed = ET.SubElement(size_in_bits, "Fixed")
            fixed_value = ET.SubElement(fixed, "FixedValue")
            fixed_value.text = str(len(obj.default) * 8)

    para_set = ET.SubElement(tm_meta, "ParameterSet")
    for obj in config.beacon_def:
        ET.SubElement(
            para_set,
            "Parameter",
            attrib={
                "name": make_obj_name(obj),
                "parameterTypeRef": make_dt_name(obj),
                "shortDescription": obj.description,
            },
        )

    cont_set = ET.SubElement(tm_meta, "ContainerSet")
    seq_cont = ET.SubElement(
        cont_set,
        "SequenceContainer",
        attrib={
            "name": "Beacon",
        },
    )
    entry_list = ET.SubElement(seq_cont, "EntryList")
    for obj in config.beacon_def:
        ET.SubElement(
            entry_list,
            "ParameterRefEntry",
            attrib={
                "parameterRef": make_obj_name(obj),
            },
        )

    # write
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    file_name = f"{config.oresat_id.name.lower()}.xtce"
    tree.write(f"{dir_path}/{file_name}", encoding="utf-8", xml_declaration=True)


def gen_xtce(sys_args=None):
    """Gen_dcf main."""

    if sys_args is None:
        sys_args = sys.argv[1:]

    parser = ArgumentParser(description=GEN_XTCE, prog=GEN_XTCE_PROG)
    parser.add_argument(
        "oresat", default="oresat0", help="oresat mission; oresat0, oresat0.5, or oresat1"
    )
    parser.add_argument("-d", "--dir-path", default=".", help='directory path; defautl "."')
    args = parser.parse_args(sys_args)

    arg_oresat = args.oresat.lower()
    if arg_oresat in ["0", "oresat0"]:
        oresat_id = OreSatId.ORESAT0
    elif arg_oresat in ["0.5", "oresat0.5"]:
        oresat_id = OreSatId.ORESAT0_5
    elif arg_oresat in ["1", "oresat1"]:
        oresat_id = OreSatId.ORESAT1
    else:
        print(f"invalid oresat mission: {args.oresat}")
        sys.exit()

    config = OreSatConfig(oresat_id)
    write_xtce(config, args.dir_path)
