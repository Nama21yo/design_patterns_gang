// Target interface - what the client expects
interface NotificationService {
  sendNotification(to: string, message: string): void;
}

// Existing in-house EmailNotificationService (Adaptee)
class EmailNotificationService {
  sendEmail(to: string, subject: string, body: string) {
    console.log(`Sending email to ${to}: [${subject}] ${body}`);
  }
}

// Third-party email service (incompatible interface)
class ThirdPartyEmailService {
  send(toAddress: string, content: string) {
    console.log(`Third-party sending email to ${toAddress}: ${content}`);
  }
}

// Adapter for ThirdPartyEmailService to conform to NotificationService interface
class ThirdPartyEmailAdapter implements NotificationService {
  private thirdPartyService: ThirdPartyEmailService;

  constructor(service: ThirdPartyEmailService) {
    this.thirdPartyService = service;
  }

  sendNotification(to: string, message: string): void {
    // Translate client request to third-party service call
    const subject = "Notification from E-Commerce App";
    const content = `${subject}\n\n${message}`;
    this.thirdPartyService.send(to, content);
  }
}

// Client code which uses NotificationService interface
class Client {
  private notificationService: NotificationService;

  constructor(notificationService: NotificationService) {
    this.notificationService = notificationService;
  }

  notifyCustomer(email: string, message: string) {
    this.notificationService.sendNotification(email, message);
  }
}

// Usage with old in-house service
const oldEmailService = new EmailNotificationService();
const clientOld = new Client({
  sendNotification: (to, message) => oldEmailService.sendEmail(to, "Notification", message)
});
clientOld.notifyCustomer("customer1@example.com", "Your order has been shipped!");

// Usage with new third-party service via Adapter
const thirdPartyService = new ThirdPartyEmailService();
const adapter = new ThirdPartyEmailAdapter(thirdPartyService);
const clientNew = new Client(adapter);
clientNew.notifyCustomer("customer2@example.com", "Your order has been delivered!");
