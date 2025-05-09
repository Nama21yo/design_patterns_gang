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

interface Role {
  getRole(): string;
}

class GoalKeeperRole implements Role {
  getRole(): string {
    return "goalkeeper";
  }
}

class DefenderRole implements Role {
  getRole(): string {
    return "defender";
  }
}

class MidfielderRole implements Role {
  getRole(): string {
    return "midfielder";
  }
}

class ForwardRole implements Role {
  getRole(): string {
    return "forward";
  }
}

class Footballer {
  constructor(public name: string, public age: number, private role: Role) {}

  getFootballerRole(): string {
    return `${this.name} is a ${this.role.getRole()}`;
  }
}

const kante = new Footballer("Kante", 31, new MidfielderRole());
console.log(kante.getFootballerRole());
const messi = new Footballer("Lionel Messi", 31, new ForwardRole());
console.log(messi.getFootballerRole());
