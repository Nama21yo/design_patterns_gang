// ! bad version of OCP
// class Footballer {
//     constructor(public name: string, public age: number, public role: string)
//  {}
//     getFootballerRole(): string {
//         switch (this.role) {
//             case "goalkeeper":
//                 return `${this.name} is a goalkeeper`
//             case "defender":
//                 return `${this.name} is a defender`
//             case "midfielder":
//                 return `${this.name} is midfielder`
//             case "forward":
//                 return `${this.name} plays  in the forward line`
//             default:
//                 throw new Error("Unsupported role")
//         }
//     }
// }

// const hazard = new Footballer("Hazard", 32, "forward")
// console.log(hazard.getFootballerRole());

// Interface-like base class for roles
class Role {
  getRole() {
    throw new Error("Method 'getRole()' must be implemented.");
  }
}

class GoalKeeperRole extends Role {
  getRole() {
    return "goalkeeper";
  }
}

class DefenderRole extends Role {
  getRole() {
    return "defender";
  }
}

class MidfielderRole extends Role {
  getRole() {
    return "midfielder";
  }
}

class ForwardRole extends Role {
  getRole() {
    return "forward";
  }
}

class Footballer {
  constructor(name, age, role) {
    this.name = name;
    this.age = age;
    this.role = role;
  }

  getFootballerRole() {
    return `${this.name} is a ${this.role.getRole()}`;
  }
}

const kante = new Footballer("Kante", 31, new MidfielderRole());
console.log(kante.getFootballerRole());

const messi = new Footballer("Lionel Messi", 31, new ForwardRole());
console.log(messi.getFootballerRole());
