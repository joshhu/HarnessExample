import { readFileSync } from "node:fs";

const files = {
  readme: readFileSync("README.md", "utf8"),
  guide: readFileSync("GUIDE.md", "utf8"),
  html: readFileSync("index.html", "utf8"),
  cart: readFileSync("src/cart.js", "utf8"),
};

const requiredConcepts = [
  "Harness",
  "Guide",
  "Sensor",
  "Feedforward",
  "Feedback",
  "Computational control",
  "Inferential control",
  "Steering loop",
  "Keep quality left",
  "Maintainability harness",
  "Architecture fitness harness",
  "Behaviour harness",
  "Harnessability",
  "Harness template",
  "Human role",
  "Context engineering",
  "Ambient affordances",
  "Ashby's Law",
  "Continuous drift",
  "Open questions",
];

const failures = [];

for (const concept of requiredConcepts) {
  if (!files.readme.includes(concept)) {
    failures.push(`README.md must mention article concept: ${concept}`);
  }
}

if (!files.guide.includes("feedforward guide")) {
  failures.push("GUIDE.md must describe itself as a feedforward guide");
}

if (!files.html.includes('type="module"')) {
  failures.push('index.html must load app.js with type="module"');
}

if (/document\.|querySelector|innerHTML|addEventListener/.test(files.cart)) {
  failures.push("src/cart.js must stay pure and must not touch DOM APIs");
}

if (failures.length > 0) {
  for (const failure of failures) {
    console.error(`[harness-fail] ${failure}`);
  }
  process.exit(1);
}

console.log("[harness-pass] guide, article checklist, and architecture boundaries passed");
