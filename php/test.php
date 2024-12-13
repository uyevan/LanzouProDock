<?php

// 设置响应头，确保返回的是 JSON 格式
header('Content-Type: application/json');

// 获取 fileId 参数
$fileId = isset($_GET['fileId']) ? intval($_GET['fileId']) : null;

if ($fileId === null) {
    echo json_encode(["code" => 400, "status" => "Missing fileId parameter"]);
    exit;
}

// 调用 iParse 函数
$result = iParse($fileId);

// 返回 JSON 格式的结果
echo json_encode($result);


/**
 * 解析文件
 */
function iParse($fileId)
{
    $rUrl = 'https://api.ilanzou.com/unproved/file/redirect';
    $rTime = round(microtime(true) * 1000);

    // 构建请求参数
    $rParams = [
        "downloadId" => aes_ecb_pkcs7_encrypt($fileId . "|", 'lanZouY-disk-app'),
        "enable" => 1,
        "devType" => 3,
        "uuid" => generate_random_string(21),
        "timestamp" => aes_ecb_pkcs7_encrypt($rTime, 'lanZouY-disk-app'),
        "auth" => aes_ecb_pkcs7_encrypt($fileId . "|" . $rTime, 'lanZouY-disk-app')
    ];

    // 拼接 URL
    $queryString = http_build_query($rParams);
    $url = $rUrl . '?' . $queryString;

    $headers = [
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept: application/json, text/plain, */*',
        'Connection: keep-alive',
        'Cookie: down_ip=1'
    ];

    // 初始化 cURL 请求
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HEADER, true); // 包含头部信息
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false); // 不自动跟随重定向
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);

    $response = curl_exec($ch);

    if ($response === false) {
        $error = curl_error($ch);
        curl_close($ch);
        return ["code" => 500, "status" => "cURL error: $error", "url" => null];
    }

    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
    $headers = substr($response, 0, $headerSize);
    $body = substr($response, $headerSize);

    curl_close($ch);

    // 处理 HTTP 状态码
    if ($httpCode == 302) {
        // 获取重定向地址
        preg_match('/Location: (.+)/', $headers, $matches);
        $redirectUrl = isset($matches[1]) ? trim($matches[1]) : null;
        return ["code" => 200, "status" => "Parse successful", "url" => $redirectUrl];
    } elseif ($httpCode == 200) {
        // 解析 JSON 响应
        $jsonResponse = json_decode($body, true);
        if (isset($jsonResponse['url'])) {
            return ["code" => 200, "status" => "Parse successful", "url" => $jsonResponse['url']];
        } elseif (isset($jsonResponse['data']['url'])) {
            return ["code" => 200, "status" => "Parse successful", "url" => $jsonResponse['data']['url']];
        }
    }

    return ["code" => 400, "status" => "Parse failed", "url" => null];
}

/**
 * AES 加密函数
 */
function aes_ecb_pkcs7_encrypt($plaintext, $key)
{
    $blockSize = 16;
    $padLength = $blockSize - (strlen($plaintext) % $blockSize);
    $paddedPlaintext = $plaintext . str_repeat(chr($padLength), $padLength);

    $encrypted = openssl_encrypt($paddedPlaintext, 'AES-128-ECB', $key, OPENSSL_RAW_DATA | OPENSSL_NO_PADDING);
    return strtoupper(bin2hex($encrypted));
}

/**
 * 随机字符串生成函数
 */
function generate_random_string($length)
{
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}
