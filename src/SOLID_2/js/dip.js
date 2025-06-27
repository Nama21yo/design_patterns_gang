// //  BAD: NotificationService depends directly on concrete classes

// class SMSService {
//   send(message) {
//     console.log(`Sending SMS: ${message}`);
//   }
// }

// class EmailService {
//   send(message) {
//     console.log(`Sending Email: ${message}`);
//   }
// }

// class NotificationService {
//   constructor() {
//     this.smsService = new SMSService();
//     this.emailService = new EmailService();
//   }

//   notifyViaSMS(message) {
//     this.smsService.send(message);
//   }

//   notifyViaEmail(message) {
//     this.emailService.send(message);
//   }
// }

// // Usage
// const badNotifier = new NotificationService();
// badNotifier.notifyViaSMS("Hello via SMS");
// badNotifier.notifyViaEmail("Hello via Email");

// Interface-like abstraction
class NotificationChannel {
  send(message) {
    throw new Error("Method 'send()' must be implemented.");
  }
}

// Concrete implementation - SMS
class SMSService extends NotificationChannel {
  send(message) {
    console.log(`Sending SMS: ${message}`);
  }
}

// Concrete implementation - Email
class EmailService extends NotificationChannel {
  send(message) {
    console.log(`Sending Email: ${message}`);
  }
}

//  NotificationService depends on abstraction, not concrete
class NotificationService {
  constructor(notificationChannel) {
    this.notificationChannel = notificationChannel;
  }

  notify(message) {
    this.notificationChannel.send(message);
  }
}

// Usage
const smsNotifier = new NotificationService(new SMSService());
smsNotifier.notify("Hello via SMS"); // ✅

const emailNotifier = new NotificationService(new EmailService());
emailNotifier.notify("Hello via Email"); // ✅
