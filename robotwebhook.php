<?php
require_once __DIR__ . '/vendor/autoload.php';
use TelegramBot\Api\BotApi;
use TelegramBot\Api\Types\Update;

$token = 'YOUR_BOT_TOKEN'; // توکن ربات خود را جایگزین کنید

$bot = new BotApi($token);

// دریافت داده از تلگرام (Webhook)
$input = file_get_contents('php://input');
$data = json_decode($input, true);

try {
    if (isset($data['message'])) {
        $message = $data['message'];
        $chatId = $message['chat']['id'];
        $text = $message['text'] ?? '';

        // دستور /start
        if ($text === '/start') {
            $bot->sendMessage($chatId, "👋 سلام! من ربات PHP شما هستم.");
        }
        // پاسخ به پیام معمولی
        else {
            $bot->sendMessage($chatId, "شما نوشتید: " . $text);
        }
    }
} catch (Exception $e) {
    error_log("خطا: " . $e->getMessage());
}
?>
