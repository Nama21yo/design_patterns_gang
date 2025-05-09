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
var GoalKeeperRole = /** @class */ (function () {
    function GoalKeeperRole() {
    }
    GoalKeeperRole.prototype.getRole = function () {
        return "goalkeeper";
    };
    return GoalKeeperRole;
}());
var DefenderRole = /** @class */ (function () {
    function DefenderRole() {
    }
    DefenderRole.prototype.getRole = function () {
        return "defender";
    };
    return DefenderRole;
}());
var MidfielderRole = /** @class */ (function () {
    function MidfielderRole() {
    }
    MidfielderRole.prototype.getRole = function () {
        return "midfielder";
    };
    return MidfielderRole;
}());
var ForwardRole = /** @class */ (function () {
    function ForwardRole() {
    }
    ForwardRole.prototype.getRole = function () {
        return "forward";
    };
    return ForwardRole;
}());
var Footballer = /** @class */ (function () {
    function Footballer(name, age, role) {
        this.name = name;
        this.age = age;
        this.role = role;
    }
    Footballer.prototype.getFootballerRole = function () {
        return "".concat(this.name, " is a ").concat(this.role.getRole());
    };
    return Footballer;
}());
var kante = new Footballer("Kante", 31, new MidfielderRole());
console.log(kante.getFootballerRole());
var messi = new Footballer("Lionel Messi", 31, new ForwardRole());
console.log(messi.getFootballerRole());
