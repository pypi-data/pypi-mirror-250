#!/bin/bash
# This script runs the linkmedic and compares the number of reported dead links with the reference value provided to it.
# if the number of reported dead links and the reference does not match, it exits with a non-zero code.
#
# requirements:
#
## which
## jq
## jsonschema [optional]

die()
{
	local _ret="${2:-1}"
	test "${_PRINT_HELP:-no}" = yes && print_help >&2
	echo "$1" >&2
	exit "${_ret}"
}

# THE DEFAULTS INITIALIZATION - POSITIONALS
_positionals=()
_arg_flags=""
# THE DEFAULTS INITIALIZATION - OPTIONALS
_arg_dead_internal_ref="0"
_arg_dead_external_ref="0"
_arg_dead_total_ref="0"
_arg_http_links_ref="0"
_arg_return_code_ref=""
_arg_launcher=""
_arg_badge_schema="badges/badge.schema.json"

print_help()
{
	printf '%s\n' "Tester script to compare the output of linkmedic with the expected values"
	printf 'Usage: %s [--dead-internal-ref <arg>] [--dead-external-ref <arg>] [--dead-total-ref <arg>] [--http-links-ref <arg>] [--return-code-ref <arg>] [--help] [<flags>]\n' "$0"
	printf '\t%s\n' "<flags>: extra linkmedic flags. '--with-badge' is always passed to the linkmedic"
	printf '\t%s\n' "--launcher: test launcher executable"
	printf '\t%s\n' "--dead-internal-ref: number of expected dead internal links (default: '0')"
	printf '\t%s\n' "--dead-external-ref: number of expected dead external links (default: '0')"
	printf '\t%s\n' "--dead-total-ref: number of expected total dead links (default: '0')"
	printf '\t%s\n' "--http-links-ref: number of expected http links (default: '0')"
	printf '\t%s\n' "--return-code-ref: override the default expected return code ('0' for tests with no dead link, '1' for tests with dead link)"
	printf '\t%s\n' "--help: print help (this list!)"
}


parse_commandline()
{
	_positionals_count=0
	while test $# -gt 0
	do
		_key="$1"
		case "$_key" in
			--launcher)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_launcher="$2"
				shiftd
				;;
			--launcher=*)
				_arg_launcher="${_key##--launcher=}"
				;;
			--badge-schema)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_badge_schema="$2"
				shiftd
				;;
			--badge-schema=*)
				_arg_badge_schema="${_key##--badge-schema=}"
				;;
			--dead-internal-ref)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_dead_internal_ref="$2"
				shift
				;;
			--dead-internal-ref=*)
				_arg_dead_internal_ref="${_key##--dead-internal-ref=}"
				;;
			--dead-external-ref)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_dead_external_ref="$2"
				shift
				;;
			--dead-external-ref=*)
				_arg_dead_external_ref="${_key##--dead-external-ref=}"
				;;
			--dead-total-ref)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_dead_total_ref="$2"
				shift
				;;
			--dead-total-ref=*)
				_arg_dead_total_ref="${_key##--dead-total-ref=}"
				;;
			--http-links-ref)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_http_links_ref="$2"
				shift
				;;
			--http-links-ref=*)
				_arg_http_links_ref="${_key##--http-links-ref=}"
				;;
			--return-code-ref)
				test $# -lt 2 && die "Missing value for the optional argument '$_key'." 1
				_arg_return_code_ref="$2"
				shift
				;;
			--return-code-ref=*)
				_arg_return_code_ref="${_key##--return-code-ref=}"
				;;				
			--help)
				print_help
				exit 0
				;;
			*)
				_last_positional="$1"
				_positionals+=("$_last_positional")
				_positionals_count=$((_positionals_count + 1))
				;;
		esac
		shift
	done
}


handle_passed_args_count()
{
	test "${_positionals_count}" -le 1 || _PRINT_HELP=yes die "FATAL ERROR: There were spurious positional arguments --- we expect between 0 and 1, but got ${_positionals_count} (the last one was: '${_last_positional}')." 1
}


assign_positional_args()
{
	local _positional_name _shift_for=$1
	_positional_names="_arg_flags "

	shift "$_shift_for"
	for _positional_name in ${_positional_names}
	do
		test $# -gt 0 || break
		eval "$_positional_name=\${1}" || die "Error during argument parsing, possibly a CLI parser bug." 1
		shift
	done
}

verify_badge_color()
{
	local _badge_info_file=$1
	local _badge_type=$2

	declare -A badge_fail_color
	badge_fail_color["critical"]="red"
	badge_fail_color["warning"]="yellow"

	declare -A badge_pass_color
	badge_pass_color["critical"]="green"
	badge_pass_color["warning"]="green"

	_badge_message=$(jq '.message' <"$_badge_info_file")	
	_badge_color=$(jq '.color' <"$_badge_info_file")

	if [ "$_badge_message" == "0" ]; then
		expected_color="${badge_pass_color["$_badge_type"]}"
	else
		expected_color="${badge_fail_color["$_badge_type"]}"
	fi

	if [ "$_badge_color" == "\"$expected_color\"" ]; then
		echo -e "${color_green}* Badge color ($_badge_color) is correct!${color_reset}"
	else
		echo -e "${color_red}* Badge color IS NOT correct!"
		echo -e "** Badge type: $_badge_type"
		echo -e "** EXPECTED: \"$expected_color\", ACTUAL: $_badge_color ${color_reset}"
		exit 1;
	fi

}

compare_badge_info_file_to_ref() 
{
	local _badge_info_file=$1
	local _ref_count=$2
	local _badge_type=$3

	local _badge_name_json=${_badge_info_file##badge.}
	local _badge_name=${_badge_name_json%.json}
	local _reported
	_reported=$(jq '.message' <"$_badge_info_file")

	if [ "$_ref_count" != "0" ]; then
		if [ "$_ref_count" != "$_reported" ]; then
			echo -e "${color_red}* Number of reported $_badge_name in $_badge_info_file IS NOT CORRECT!"
			echo -e "** EXPECTED: $_ref_count, REPORTED: $_reported ${color_reset}"
			exit 1;
		else
			echo -e "${color_green}* Number of reported $_badge_name in $_badge_info_file is correct!"
			echo -e "** EXPECTED: $_ref_count, REPORTED: $_reported ${color_reset}"
		fi
	elif [ "$_reported" != "0" ]; then
		echo -e "${color_red}* UNEXPECTED DEAD LINKS REPORTED IN BADGE INFO FILE \"$_badge_info_file\"!"
		echo -e "** EXPECTED: 0, REPORTED: $_reported ${color_reset}"
		exit 1;
	fi
}

validate_badge_info_file()
{
	local _badge_info_file=$1
	local _ref_count=$2
	local _badge_type=$3

	if [ -f "$_badge_info_file" ]; then
		if [[ -x "$(command -v jsonschema)" ]]; then
			if jsonschema -i "$(realpath "$_badge_info_file")" "$_arg_badge_schema"; then
				echo -e "${color_green}* Generated badge info file ($_badge_info_file) conforms to the schema.${color_reset}"
			else
				echo -e "${color_red}* BADGE INFO FILE ($_badge_info_file) DOES NOT CONFORM TO THE PROVIDED SCHEMA ($_arg_badge_schema)!${color_reset}"
				exit 1;
			fi
		else
			echo -e "${color_yellow}* jsonschema was not found! Skipping schema verification...${color_reset}"
		fi
		compare_badge_info_file_to_ref "$_badge_info_file" "$_ref_count" "$_badge_type"
		verify_badge_color "$_badge_info_file" "$_badge_type"
		
	elif [ "$_ref_count" != "0" ]; then
		echo -e "${color_red}* BADGE INFO FILE $_badge_info_file WAS NOT FOUND!${color_reset}"
		exit 1;
	fi
}


parse_commandline "$@"
handle_passed_args_count
assign_positional_args 1 "${_positionals[@]}"

color_red="\033[31;49;1m"
color_green="\033[32;49;1m"
color_yellow="\033[33;49;1m"
color_reset="\033[0m"

if [ -n "$_arg_return_code_ref" ]; then
	expected_return_code="$_arg_return_code_ref"
else
	if [ "$_arg_dead_internal_ref" = "0" ] && [ "$_arg_dead_external_ref" = "0" ] && [ "$_arg_dead_total_ref" = "0" ]; then
		expected_return_code="0"
	else
		expected_return_code="1"
	fi
fi
echo "============================================================"
echo "* Expected internal dead links: $_arg_dead_internal_ref"
echo "* Expected external dead links: $_arg_dead_external_ref"
echo "* Expected total dead links   : $_arg_dead_total_ref"
echo "* Expected return code        : $expected_return_code"
echo "* Expected HTTP links         : $_arg_http_links_ref"
echo "* Test launcher               : $_arg_launcher"
echo "* linkmedic flags             : $_arg_flags"
echo "============================================================"

IFS=' ' read -ra _arg_flags_list <<< "$_arg_flags"
# cleanup env.
rm -f badge.*

# shellcheck disable=2086
command $_arg_launcher "linkmedic" "${_arg_flags_list[@]}" "--with-badge"
linkmedic_return_code=$?
echo "* linkmedic return code = $linkmedic_return_code"

# TODO: fix logs logic (for when --return-code-ref is explicit)
if [[ "$_arg_return_code_ref" -ge 2 ]]; then
	if [ "$linkmedic_return_code" != "$_arg_return_code_ref" ]; then
		echo -e "${color_red}* Unexpected return code!"
		echo -e "** EXPECTED: $_arg_return_code_ref, RETURNED: $linkmedic_return_code ${color_reset}"
		fatal=1
	fi
	echo -e "${color_green}* Return code is as expected!${color_reset}"
else
	if [[ "$expected_return_code" == "0" ]]; then
		if [[ "$linkmedic_return_code" != "0" ]]; then
			echo -e "${color_red}* Unexpected links checker failure! Either unexpected dead links are reported or the link checker exited unexpectedly!${color_reset}" 
			fatal=1
		fi
		echo -e "${color_green}* As expected, no dead links were reported!${color_reset}"
	elif [[ "$expected_return_code" == "1" ]]; then
		if [[ "$linkmedic_return_code" == "0" ]]; then
			echo -e "${color_red}* Some dead links were not reported!${color_reset}"
			fatal=1
		fi
		echo -e "${color_green}* As expected, dead links were reported!${color_reset}"
	fi

	if [[ "$fatal" == "1" ]]; then
		echo "* Restarting the test with debug logging"
		command $_arg_launcher "linkmedic" "${_arg_flags_list[@]}" "-v" "--with-badge"
		exit 1;
	fi

	validate_badge_info_file "badge.dead_internal_links.json" "$_arg_dead_internal_ref" "critical"
	validate_badge_info_file "badge.dead_external_links.json" "$_arg_dead_external_ref" "critical"
	validate_badge_info_file "badge.dead_links.json" "$_arg_dead_total_ref" "critical"
	validate_badge_info_file "badge.http_links.json" "$_arg_http_links_ref" "warning"
fi
