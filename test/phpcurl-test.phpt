<?php

$file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/results/php.csv';
$curl_file = '/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/results/curl.out';

if (file_exists($file)) {
	unlink($file);
}
if (file_exists($curl_file)) {
	unlink($curl_file);
}

$json = file_get_contents('/home/dashmeetkaur/Desktop/urlparse/url-parsing/test/tests.json');
$json = str_replace("\u", "\\\\u", $json);
$data = json_decode($json, true);
$parsed_urls = array();

$urls = $data['urls'];
foreach ($urls as $url) {
	$parsed = parse_url($url);
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
	}
	else {
		$parsed = array("scheme" => "Not Parsed. Return: false");
	}
	$parsed_urls[] = [$url, print_r($parsed, true)];

	// CURL
	$curl = curl_init();
	$curl_log = fopen($curl_file, 'a');

	fwrite($curl_log, $url);
	fwrite($curl_log, "\n");
	curl_setopt_array($curl, array(
		CURLOPT_URL             => $url,
		CURLOPT_VERBOSE         => 1,
		CURLOPT_STDERR          => $curl_log,
		CURLOPT_FILE            => $curl_log,
		CURLOPT_CONNECTTIMEOUT  => 2,
		CURLOPT_NOBODY  => True,
		CURLOPT_HEADER  => True
	));
	curl_exec($curl);
	if ($e = curl_errno($curl)) {
		fwrite($curl_log, curl_strerror($e));
	}
	fwrite($curl_log, "\n\n-------------\n");
	fclose($curl_log);
	curl_close($curl);
}

write_to_csv($parsed_urls);
print("Done!\nCheck files ". $file . " and " . $curl_file . " for details.\n");

function write_to_csv($parsed_urls) {
	global $file;
	$fp = fopen($file, 'w+');
	$header = array('URL', 'PHP');
	fputcsv($fp, $header, ',');
	foreach ($parsed_urls as $parsed_url) {
		fputcsv($fp, $parsed_url, ',');
	}
	fclose($fp);
}

?>