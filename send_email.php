<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'vendor/autoload.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars(trim($_POST['name']));
    $email = htmlspecialchars(trim($_POST['email']));
    $phone = htmlspecialchars(trim($_POST['phone']));
    $message = htmlspecialchars(trim($_POST['message']));

    $mail = new PHPMailer(true);
    try {
        $mail->isSMTP();
        $mail->Host = 'smtp.zoho.com';
        $mail->SMTPAuth = true;
        $mail->Username = 'office@dodadigital.kz';
        $mail->Password = 'ZohoDoda12345!'; // Пароль от Zoho Mail или App Password
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port = 587;

        $mail->setFrom('office@dodadigital.kz', 'DODA Digital');
        $mail->addAddress('office@dodadigital.kz');
        $mail->addReplyTo($email, $name);

        $mail->isHTML(false);
        $mail->Subject = 'Новая заявка с сайта DODA Digital';
        $mail->Body = "Имя: $name\nEmail: $email\nТелефон: $phone\nСообщение:\n$message";

        $mail->send();
        http_response_code(200);
        echo json_encode(["message" => "Заявка успешно отправлена"]);
    }
    catch (Exception $e) {
        http_response_code(500);
        echo json_encode(["message" => "Ошибка при отправке заявки: {$mail->ErrorInfo}"]);
    }
} 
else {
    http_response_code(400);
    echo json_encode(["message" => "Неверный метод запроса"]);
}
?>
