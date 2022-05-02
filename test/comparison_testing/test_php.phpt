<?php

if ($argc == 1) {
	print("Usage: php test_php.phpt [library name to test with]\n");
	exit();
}

$lib_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/extract_urls/testsuite_results/' . $argv[1] . '.json';
$diff_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/comparison_testing/diffs/diff_php_' . $argv[1] . '.csv';

if (file_exists($diff_file)) {
	unlink($diff_file);
}

$data = json_decode(file_get_contents($lib_file), true);
if (json_last_error()) {
	$json = file_get_contents($lib_file);
	$json = str_replace("\u", "\\\\u", $json);
	$data = json_decode($json, true);
}

$urls = $data['urls'];
$diff_count = 0;
$total_count = 0;

foreach ($urls as $url) {
	global $total_count;

	$input_url = $url['input'];
	$parsed = parse_url($input_url);
    $total_count += 1;

    if ($parsed) {
		$keys = array('scheme', 'user', 'password', 'host', 'port', 'path', 'query', 'fragment');
	    if (isset($parsed["pass"])) {
	    	$parsed["password"] = $parsed["pass"];
	    	unset($parsed["pass"]);
	    }
	    foreach ($keys as $key) {
	    	if (!isset($parsed[$key])) {
	    		$parsed[$key] = "";
	    	}
	    }
		compare_parser_outputs($input_url, $parsed, $url['expected_output']);
	} else {
		compare_parser_outputs($input_url, array("scheme" => "Not Parsed. Return: false"), $url['expected_output']);
	}
}
print("\nOut of total " . $total_count . ", found " . $diff_count . " differences in parsing. Check file ". $diff_file . " for details.\n");

function compare_parser_outputs($url, $php_output, $lib_output) {
	global $diff_count;

	$mismatch = 0;
	foreach ($php_output as $key => $value) {
		// if (!isset($lib_output[$key])) {
		// 	$lib_output[$key] = '';
		// }
		if ($value != $lib_output[$key]) {
			$mismatch = 1;
		}
	}

	if ($mismatch == 1) {
		$diff_count += 1;
		$diff = array($url, print_r($lib_output, true), print_r($php_output, true));
		write_to_csv($diff);
	}
}

function write_to_csv($diff) {
	global $diff_file;
	global $argv;

	if(!file_exists($diff_file)) {
		$fp = fopen($diff_file, 'a+');
		$header = array('URL', $argv[1], 'php');
		fputcsv($fp, $header, ',');
		fclose($fp);
	}
	$fp = fopen($diff_file, 'a+');
	fputcsv($fp, $diff, ',');
	fclose($fp);
}

?>