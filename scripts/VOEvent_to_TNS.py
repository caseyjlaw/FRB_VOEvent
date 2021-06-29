import voeventparse
import json
import argparse

tns_dict = {
  "frb_report": {
    "0": {
      "ra": {
        "value": "",
        "error": "",
        "units": "arcsec"
      },
      "dec": {
        "value": "",
        "error": "",
        "units": "arcsec"
      },
      "reporting_groupid": "",
      "groupid": "",
      "internal_name": "",
      "at_type": "5",
      "reporter": "",
      "discovery_datetime": "",
      "barycentric_event_time": "",
      "end_prop_period": "",
      "proprietary_period_groups": "",
      "transient_redshift": "",
      "host_name": "",
      "host_redshift": "",
      "repeater_of_objid": "",
      "public_webpage": "",
      "region_ellipse": "",
      "region_ellipse_unitid": "27",
      "region_polygon": "",
      "region_filename": "",
      "dm": "",
      "dm_err": "",
      "dm_unitid": "25",
      "galactic_max_dm": "",
      "galactic_max_dm_model": "",
      "remarks": "",
      "photometry": {
        "photometry_group": {
          "0": {
            "obsdate": "",
            "flux": "",
            "flux_error": "",
            "limiting_flux": "",
            "flux_units": "",
            "filter_value": "",
            "instrument_value": "",
            "snr": "",
            "fluence": "",
            "fluence_err": "",
            "fluence_unitid": "22",
            "exptime": "",
            "observer": "",
            "burst_width": "",
            "burst_width_err": "",
            "burst_width_unitid": "23",
            "burst_bandwidth": "",
            "burst_bandwidth_err": "",
            "burst_bandwidth_unitid": "24",
            "scattering_time": "",
            "scattering_time_err": "",
            "scattering_time_unitid": "23",
            "dm_struct": "",
            "dm_struct_err": "",
            "dm_struct_unitid": "25",
            "rm": "",
            "rm_err": "",
            "rm_unitid": "26",
            "frac_lin_pol": "",
            "frac_lin_pol_err": "",
            "frac_circ_pol": "",
            "frac_circ_pol_err": "",
            "ref_freq": "",
            "ref_freq_unitid": "24",
            "inst_bandwidth": "",
            "inst_bandwidth_unitid": "24",
            "channels_no": "",
            "sampling_time": "",
            "sampling_time_unitid": "23",
            "comments": ""
          },
        }
      },
#      "related_files": {
#        "0": {
#          "related_file_name": "",
#          "related_file_comments": ""
#        },
#      }
    }
  }
}

def get_voevent(inname):
    """ Use voeventparse to read voevent.
    """

    with open(inname, 'rb') as fp:
        ve = voeventparse.load(fp)

    return ve


def set_dict(ve, groupid, phot_dict={}, event_dict={}):
    """ assign values to TNS dictionary. Most values taken from parsed VOEvent file.
    - groupid is associated with bot registred with TNS (used for "reporting_groupid" and "groupid").

    Optional dictionary input to overload some fields:
    - phot_dict is dictionary for "photometry" keys to set: "snr", "flux", "flux_error", "fluence", "burst_width", "sampling_time".
    - event_dict is dictionary for other TNS keys (from frb_report set): "internal_name", "reporter", "remarks", "host_name", "repeater_of_objid".
    """

    tns_dict['frb_report']['0']["internal_name"] = str(ve.Why.Name)
    tns_dict['frb_report']['0']["reporter"] = "Casey J. Law"
    pos = voeventparse.get_event_position(ve)
    tns_dict['frb_report']['0']['ra']['value'] = pos.ra
    tns_dict['frb_report']['0']['dec']['value'] = pos.dec
    tns_dict['frb_report']['0']['ra']['error'] = pos.err
    tns_dict['frb_report']['0']['dec']['error'] = pos.err
    dt = voeventparse.get_event_time_as_utc(ve)
    dtstring = f'{dt.date().isoformat()} {dt.time().isoformat()}'
    tns_dict['frb_report']['0']["discovery_datetime"] = dtstring
    tns_dict['frb_report']['0']["reporting_groupid"] = groupid
    tns_dict['frb_report']['0']["groupid"] = groupid
    tns_dict['frb_report']['0']["at_type"] = "5"  # FRBs

    params = voeventparse.get_grouped_params(ve)
    tns_dict['frb_report']['0']["dm"] = params['event parameters']['dm']['value']
    try:
        tns_dict['frb_report']['0']["dmerr"] = params['event parameters']['dm_error']['value']
    except KeyError:
        pass
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["snr"] = params['event parameters']['snr']['value']
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["burst_width"] = params['event parameters']['width']['value']
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["filter_value"] = 129
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["instrument_value"] = 239
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["flux"] = 0   # TODO: set this
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["flux_error"] = 0   # TODO: set this
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["limiting_flux"] = 0
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["obsdate"] = dtstring
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["flux_units"] = "Jy"
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["ref_freq"] = "1405"
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["inst_bandwidth"] = "250"
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["channels_no"] = 1024
    tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]["sampling_time"] = 1

    # set photometry values
    for key, value in phot_dict.items():
        if key in tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"]:
            print(f'Overloading event key {key} with {value}')
            tns_dict['frb_report']['0']["photometry"]["photometry_group"]["0"][key] = value
            
    # overload other values
    for key, value in event_dict.items():
        if key in tns_dict['frb_report']['0']:
            print(f'Overloading event key {key} with {value}')
            tns_dict['frb_report']['0'][key] = value
            
    return tns_dict


def write_tns(dd, outname):
    """ Use json to write TNS dict
    """

    with open(outname, 'w') as fp:
        json.dump(dd, fp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input VOEvent xml file name")
    parser.add_argument("groupid", help="TNS groupid")
    parser.add_argument("outfile", help="output json file name")
    args = parser.parse_args()


    ve = get_voevent(args.infile)
    dd = set_dict(ve, args.groupid)
    write_tns(dd, args.outfile)
