const session = readSession();

const levelLabels = {
  high_school: "High School (8th - 10th)",
  intermediate: "Intermediate / PUC (11th - 12th)",
  undergraduate: "Undergraduate Student",
  job_seeker: "Job Seeker",
  higher_studies: "Higher Studies Aspirant",
};

const levelAliases = {
  "High School": levelLabels.high_school,
  "High School (8th - 10th)": levelLabels.high_school,
  "Intermediate / PUC": levelLabels.intermediate,
  "Intermediate / PUC (11th - 12th)": levelLabels.intermediate,
  Undergraduate: levelLabels.undergraduate,
  "Undergraduate Student": levelLabels.undergraduate,
  Postgraduate: levelLabels.higher_studies,
  "Higher Studies Aspirant": levelLabels.higher_studies,
  Other: levelLabels.job_seeker,
};

const intermediateSubjects = {
  MPC: ["Mathematics", "Physics", "Chemistry"],
  BiPC: ["Biology", "Physics", "Chemistry"],
  MEC: ["Mathematics", "Economics", "Commerce"],
  CEC: ["Civics", "Economics", "Commerce"],
  HEC: ["History", "Economics", "Civics"],
};

const branchesByDegree = {
  "B.Tech": ["CSE", "AIML", "ECE", "EEE", "Mechanical", "Civil", "IT"],
  "B.Sc": ["Computer Science", "Data Science", "Mathematics", "Physics", "Biotechnology"],
  BCA: ["Computer Applications", "Data Science", "Cloud Computing"],
  "B.Com": ["Commerce", "Finance", "Business Analytics"],
  BA: ["Economics", "Psychology", "English", "Public Policy"],
  BBA: ["Marketing", "Finance", "Business Analytics", "Entrepreneurship"],
};

const skillsByBranch = {
  CSE: ["Python", "Java", "C++", "SQL", "DSA", "Web Development", "Machine Learning", "Deep Learning", "Cloud Computing", "Cyber Security", "Data Analysis", "Statistics"],
  AIML: ["Python", "SQL", "DSA", "Machine Learning", "Deep Learning", "Data Analysis", "Statistics", "Cloud Computing", "Research"],
  IT: ["Python", "Java", "SQL", "DSA", "Web Development", "Cloud Computing", "Cyber Security", "Linux", "Networking"],
  ECE: ["Embedded Systems", "VLSI", "IoT", "Communication Systems", "Python", "Networking", "Research"],
  EEE: ["Power Systems", "Control Systems", "Electrical Machines", "IoT", "Embedded Systems"],
  Mechanical: ["CAD", "SolidWorks", "Manufacturing", "Thermodynamics", "Data Analysis", "Research"],
  Civil: ["AutoCAD", "Structural Analysis", "Surveying", "Construction Management", "Data Analysis"],
  "Computer Science": ["Python", "SQL", "DSA", "Web Development", "Machine Learning", "Data Analysis", "Statistics"],
  "Data Science": ["Python", "SQL", "Machine Learning", "Data Analysis", "Statistics", "Power BI"],
  Mathematics: ["Statistics", "Python", "Data Analysis", "Research"],
  Physics: ["Research", "Python", "Data Analysis", "Communication"],
  Biotechnology: ["Research", "Data Analysis", "Python", "Communication"],
  "Computer Applications": ["Python", "Java", "SQL", "Web Development", "Cloud Computing"],
  "Cloud Computing": ["Cloud Computing", "Linux", "Networking", "Python", "AWS"],
  Commerce: ["Excel", "Data Analysis", "Communication", "Presentation"],
  Finance: ["Excel", "Data Analysis", "SQL", "Communication"],
  "Business Analytics": ["SQL", "Excel", "Data Analysis", "Power BI", "Presentation"],
  Economics: ["Data Analysis", "Research", "Communication", "Presentation"],
  Psychology: ["Research", "Communication", "Data Analysis"],
  English: ["Communication", "Presentation", "Research"],
  "Public Policy": ["Research", "Communication", "Data Analysis", "Leadership"],
  Marketing: ["Communication", "Presentation", "Data Analysis", "Content Strategy"],
  Entrepreneurship: ["Leadership", "Communication", "Presentation", "Data Analysis"],
};

const higherSubjectsByBranch = {
  CSE: ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "AI", "Machine Learning", "Software Engineering"],
  AIML: ["Data Structures", "AI", "Machine Learning", "Deep Learning", "Python", "Statistics"],
  ECE: ["VLSI", "Signals", "Embedded Systems", "Digital Electronics"],
  EEE: ["Power Systems", "Control Systems", "Electrical Machines", "Digital Electronics"],
  Mechanical: ["Thermodynamics", "Manufacturing", "CAD", "Fluid Mechanics"],
  Civil: ["Structures", "Surveying", "Geotechnical Engineering", "Construction Materials"],
  IT: ["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Software Engineering"],
};

const sharedCertifications = ["NPTEL", "Coursera", "Udemy", "AWS", "Google", "Microsoft"];
const jobSkillOptions = ["Python", "Java", "JavaScript", "SQL", "DSA", "Web Development", "Cloud Computing", "AWS", "Linux", "Networking", "Cyber Security", "Machine Learning", "Data Analysis", "Power BI", "Excel", "Communication", "Presentation", "Leadership", "Research"];

const schemas = {
  high_school: {
    label: levelLabels.high_school,
    title: "High School",
    description: "Enter school details.",
    guide: ["Academic Performance 30%", "Favorite Subjects 25%", "Activities 20%", "Strength Areas 25%"],
    steps: [
      {
        title: "Basic Information",
        description: "Basic details.",
        fields: [
          { type: "text", label: "Name", path: "basic_info.name", required: true },
          { type: "text", label: "Class", path: "basic_info.class_level", required: true, placeholder: "Example: 10th" },
          { type: "text", label: "School", path: "basic_info.school", required: true },
        ],
      },
      {
        title: "Academic Performance",
        description: "Marks out of 100.",
        fields: [{ type: "marks", label: "Subject Marks", path: "marks", subjects: ["Mathematics", "Science", "English", "Social Studies", "Computer Science", "Biology"] }],
      },
      {
        title: "Interests",
        description: "Select interests.",
        fields: [
          { type: "chips", label: "Favorite Subjects", path: "favorite_subjects", required: true, options: ["Mathematics", "Science", "Biology", "Computer Science", "English", "Social Studies", "Economics"] },
          { type: "chips", label: "Activities", path: "activities", required: true, options: ["Sports", "Debates", "Drawing", "Coding", "Robotics", "Music", "Dance", "Volunteering", "Leadership Activities"] },
        ],
      },
      {
        title: "Strength Areas",
        description: "Rate 1 to 5.",
        fields: [{ type: "ratings", label: "Strength Areas", path: "strengths", items: ["Problem Solving", "Creativity", "Communication", "Leadership", "Teamwork", "Critical Thinking"] }],
      },
    ],
  },
  intermediate: {
    label: levelLabels.intermediate,
    title: "Intermediate",
    description: "Enter stream details.",
    guide: ["Subject Marks 35%", "Interests 25%", "Skills 20%", "Career Goal 20%"],
    steps: [
      {
        title: "Stream",
        description: "Select stream and marks.",
        fields: [
          { type: "select", label: "Stream", path: "stream", required: true, options: ["MPC", "BiPC", "MEC", "CEC", "HEC"], rerender: true },
          { type: "marks", label: "Subject Marks", path: "subject_marks", subjects: (data) => intermediateSubjects[data.stream] || [] },
        ],
      },
      {
        title: "Interests",
        description: "Select interests and skills.",
        fields: [
          { type: "chips", label: "Interest Areas", path: "interest_areas", required: true, options: ["AI", "Software", "Healthcare", "Finance", "Business", "Law", "Research", "Design", "Government Services"] },
          { type: "chips", label: "Skills", path: "skills", required: true, options: ["Logical Reasoning", "Communication", "Leadership", "Creativity", "Problem Solving"] },
        ],
      },
      {
        title: "Career Goal",
        description: "Optional.",
        fields: [{ type: "textarea", label: "Career Goal", path: "career_goal", required: false, placeholder: "Your goal" }],
      },
    ],
  },
  undergraduate: {
    label: levelLabels.undergraduate,
    title: "Undergraduate",
    description: "Enter readiness details.",
    guide: ["CGPA 20%", "Skills 30%", "Projects 15%", "Internships 15%", "Certifications 10%", "Interests 10%"],
    steps: [
      {
        title: "Academic Details",
        description: "Select degree and branch.",
        fields: [
          { type: "select", label: "Degree", path: "degree", required: true, options: Object.keys(branchesByDegree), rerender: true },
          { type: "select", label: "Branch", path: "branch", required: true, options: (data) => branchesByDegree[data.degree] || [], rerender: true },
          { type: "number", label: "CGPA", path: "cgpa", required: true, min: 0, max: 10, step: 0.01 },
          { type: "number", label: "Current Year", path: "current_year", required: true, min: 1, max: 6, step: 1 },
          { type: "number", label: "Backlogs", path: "backlogs", required: true, min: 0, max: 30, step: 1 },
        ],
      },
      {
        title: "Skills",
        description: "Select skills.",
        fields: [
          { type: "chips", label: "Technical Skills", path: "technical_skills", required: true, options: (data) => skillsByBranch[data.branch] || jobSkillOptions },
          { type: "chips", label: "Certifications", path: "certifications", required: false, options: sharedCertifications },
        ],
      },
      {
        title: "Readiness",
        description: "Add projects and goals.",
        fields: [
          { type: "number", label: "Projects", path: "projects", required: true, min: 0, max: 100, step: 1 },
          { type: "number", label: "Internships", path: "internships", required: true, min: 0, max: 50, step: 1 },
          { type: "chips", label: "Career Interests", path: "career_interests", required: true, options: ["AI Engineer", "Data Scientist", "Software Engineer", "Cyber Security Analyst", "Cloud Engineer", "Product Manager", "Research Engineer"] },
        ],
      },
    ],
  },
  job_seeker: {
    label: levelLabels.job_seeker,
    title: "Job Seeker Readiness",
    description: "Enter job details.",
    guide: ["Experience 20%", "Skills 30%", "Projects 15%", "Certifications 15%", "Resume Score 20%"],
    steps: [
      {
        title: "Experience",
        description: "Add education and experience.",
        fields: [
          { type: "text", label: "Degree", path: "education.degree", required: true },
          { type: "text", label: "Branch", path: "education.branch", required: true },
          { type: "number", label: "CGPA", path: "education.cgpa", required: true, min: 0, max: 10, step: 0.01 },
          { type: "number", label: "Years of Experience", path: "experience_years", required: true, min: 0, max: 50, step: 0.5 },
        ],
      },
      {
        title: "Skills",
        description: "Add skills and projects.",
        fields: [
          { type: "chips", label: "Current Skills", path: "current_skills", required: true, options: jobSkillOptions },
          { type: "number", label: "Projects", path: "projects", required: true, min: 0, max: 100, step: 1 },
          { type: "chips", label: "Certifications", path: "certifications", required: false, options: sharedCertifications },
        ],
      },
      {
        title: "Preferences",
        description: "Add resume and preferences.",
        fields: [
          { type: "file", label: "Resume Upload", path: "resume", required: true, accept: ".pdf,.doc,.docx" },
          { type: "select", label: "Preferred Industry", path: "preferred_industry", required: true, options: ["IT", "Banking", "Healthcare", "Manufacturing", "Government", "Research"] },
          { type: "text", label: "Preferred Location", path: "preferred_location", required: true },
          { type: "number", label: "Expected Salary", path: "expected_salary", required: true, min: 0, step: 1000 },
        ],
      },
    ],
  },
  higher_studies: {
    label: levelLabels.higher_studies,
    title: "Higher Studies",
    description: "Enter study details.",
    guide: ["CGPA 20%", "Subject Marks 30%", "Research Interests 20%", "Projects 15%", "Publications 15%"],
    steps: [
      {
        title: "Academic Profile",
        description: "Select academic profile.",
        fields: [
          { type: "select", label: "Degree", path: "degree", required: true, options: ["B.Tech", "B.Sc", "BCA", "B.Com", "BA", "BBA", "M.Sc", "MCA"], rerender: true },
          { type: "select", label: "Branch", path: "branch", required: true, options: Object.keys(higherSubjectsByBranch), rerender: true },
          { type: "number", label: "CGPA", path: "cgpa", required: true, min: 0, max: 10, step: 0.01 },
        ],
      },
      {
        title: "Marks",
        description: "Enter subject marks.",
        fields: [{ type: "marks", label: "Subject Marks", path: "subject_marks", subjects: (data) => higherSubjectsByBranch[data.branch] || [] }],
      },
      {
        title: "Goals",
        description: "Add goals and research.",
        fields: [
          { type: "chips", label: "Research Interests", path: "research_interests", required: true, options: ["Artificial Intelligence", "Data Science", "Robotics", "Cyber Security", "Cloud Computing", "VLSI", "Embedded Systems"] },
          { type: "number", label: "Research Publications", path: "research_publications", required: true, min: 0, max: 100, step: 1 },
          { type: "number", label: "Projects", path: "projects", required: true, min: 0, max: 100, step: 1 },
          { type: "select", label: "Higher Study Goal", path: "higher_study_goal", required: true, options: ["M.Tech", "MS", "MBA", "PhD"] },
          { type: "select", label: "Preferred Country", path: "preferred_country", required: true, options: ["India", "USA", "UK", "Germany", "Canada", "Australia"] },
        ],
      },
    ],
  },
};

const elements = {
  form: document.getElementById("assessmentForm"),
  academicLevel: document.getElementById("academicLevel"),
  wizardTitle: document.getElementById("wizardTitle"),
  wizardDescription: document.getElementById("wizardDescription"),
  wizardPanel: document.getElementById("wizardPanel"),
  stepTabs: document.getElementById("stepTabs"),
  progressText: document.getElementById("progressText"),
  progressPercent: document.getElementById("progressPercent"),
  progressFill: document.getElementById("wizardProgress"),
  guideTitle: document.getElementById("guideTitle"),
  guideText: document.getElementById("guideText"),
  criteriaList: document.getElementById("criteriaList"),
  message: document.getElementById("formMessage"),
  prevButton: document.getElementById("prevButton"),
  nextButton: document.getElementById("nextButton"),
  submitButton: document.getElementById("submitButton"),
  loadingState: document.getElementById("loadingState"),
};

let activeLevelKey = "";
let currentStep = 0;
let formData = {};
let chipSearch = {};

function readSession() {
  try {
    return JSON.parse(localStorage.getItem("career_session"));
  } catch {
    return null;
  }
}

function requireSession() {
  if (!session || !session.user) {
    window.location.replace("/login");
    return null;
  }
  return session;
}

function initials(name) {
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join("");
}

function setMessage(message, type = "") {
  elements.message.textContent = message;
  elements.message.className = `form-message ${type}`.trim();
}

function getApiError(data) {
  if (Array.isArray(data.detail)) {
    return data.detail.map((item) => item.msg).join(" ");
  }
  return data.detail || "Unable to process assessment.";
}

function levelKeyFromLabel(label) {
  return Object.entries(levelLabels).find(([, value]) => value === label)?.[0] || "";
}

function getNested(path) {
  return path.split(".").reduce((target, key) => (target && target[key] !== undefined ? target[key] : undefined), formData);
}

function setNested(path, value) {
  const keys = path.split(".");
  const last = keys.pop();
  let target = formData;
  keys.forEach((key) => {
    if (!target[key] || typeof target[key] !== "object" || Array.isArray(target[key])) {
      target[key] = {};
    }
    target = target[key];
  });
  target[last] = value;
}

function ensureArray(path) {
  const value = getNested(path);
  if (!Array.isArray(value)) {
    setNested(path, []);
    return [];
  }
  return value;
}

function defaultDataFor(levelKey) {
  if (levelKey === "high_school") {
    return {
      basic_info: {
        name: session?.user?.full_name || "",
        class_level: "",
        school: "",
      },
      marks: {},
      favorite_subjects: [],
      activities: [],
      strengths: {},
    };
  }
  if (levelKey === "intermediate") {
    return { stream: "", subject_marks: {}, interest_areas: [], skills: [], career_goal: "" };
  }
  if (levelKey === "undergraduate") {
    return { degree: "", branch: "", cgpa: "", current_year: "", backlogs: 0, technical_skills: [], certifications: [], projects: "", internships: "", career_interests: [] };
  }
  if (levelKey === "job_seeker") {
    return { education: { degree: "", branch: "", cgpa: "" }, experience_years: "", current_skills: [], projects: "", certifications: [], resume: {}, preferred_industry: "", preferred_location: "", expected_salary: "" };
  }
  if (levelKey === "higher_studies") {
    return { degree: "", branch: "", cgpa: "", subject_marks: {}, research_interests: [], research_publications: "", projects: "", higher_study_goal: "", preferred_country: "" };
  }
  return {};
}

function getOptions(field) {
  return typeof field.options === "function" ? field.options(formData) : field.options || [];
}

function getSubjects(field) {
  return typeof field.subjects === "function" ? field.subjects(formData) : field.subjects || [];
}

function normalizeDependentState(changedPath = "") {
  if (activeLevelKey === "intermediate" && changedPath === "stream") {
    formData.subject_marks = {};
  }

  if (activeLevelKey === "undergraduate") {
    if (changedPath === "degree") {
      formData.branch = "";
      formData.technical_skills = [];
    }
    if (changedPath === "branch") {
      formData.technical_skills = [];
    }
  }

  if (activeLevelKey === "higher_studies" && changedPath === "branch") {
    formData.subject_marks = {};
  }
}

function renderAll() {
  const schema = schemas[activeLevelKey];

  if (!schema) {
    elements.wizardTitle.textContent = "Select your academic level";
    elements.wizardDescription.textContent = "Choose a level to begin.";
    elements.wizardPanel.innerHTML = '<div class="empty-state">Select a level.</div>';
    elements.stepTabs.innerHTML = "";
    elements.progressText.textContent = "Step 1 of 1";
    elements.progressPercent.textContent = "0%";
    elements.progressFill.style.width = "0%";
    elements.guideTitle.textContent = "Weights";
    elements.guideText.textContent = "Level-based scoring.";
    elements.criteriaList.innerHTML = "<li>Select a level.</li>";
    elements.prevButton.disabled = true;
    elements.nextButton.disabled = true;
    elements.submitButton.classList.add("hidden");
    return;
  }

  elements.wizardTitle.textContent = schema.title;
  elements.wizardDescription.textContent = schema.description;
  elements.guideTitle.textContent = "Weights";
  elements.guideText.textContent = schema.label;
  elements.criteriaList.innerHTML = schema.guide.map((item) => `<li>${item}</li>`).join("");

  renderTabs(schema);
  renderStep(schema);
  renderProgress(schema);
  renderActions(schema);
}

function renderTabs(schema) {
  elements.stepTabs.innerHTML = schema.steps
    .map((step, index) => `<span class="step-tab ${index === currentStep ? "active" : ""}">${index + 1}. ${step.title}</span>`)
    .join("");
}

function renderProgress(schema) {
  const total = schema.steps.length;
  const percent = Math.round(((currentStep + 1) / total) * 100);
  elements.progressText.textContent = `Step ${currentStep + 1} of ${total}`;
  elements.progressPercent.textContent = `${percent}%`;
  elements.progressFill.style.width = `${percent}%`;
}

function renderActions(schema) {
  elements.prevButton.disabled = currentStep === 0;
  elements.nextButton.classList.toggle("hidden", currentStep === schema.steps.length - 1);
  elements.submitButton.classList.toggle("hidden", currentStep !== schema.steps.length - 1);
}

function renderStep(schema) {
  const step = schema.steps[currentStep];
  elements.wizardPanel.innerHTML = `
    <div class="wizard-step-heading">
      <h3>${step.title}</h3>
      <p>${step.description}</p>
    </div>
    <div class="field-grid" id="fieldGrid"></div>
  `;

  const grid = document.getElementById("fieldGrid");
  step.fields.forEach((field) => {
    grid.appendChild(renderField(field));
  });
}

function renderField(field) {
  if (field.type === "marks") {
    return renderMarks(field);
  }
  if (field.type === "ratings") {
    return renderRatings(field);
  }
  if (field.type === "chips") {
    return renderChips(field);
  }
  if (field.type === "file") {
    return renderFile(field);
  }

  const wrapper = document.createElement("div");
  wrapper.className = field.type === "textarea" ? "input-group field-wide" : "input-group";
  const value = getNested(field.path) ?? "";
  const options = getOptions(field);

  if (field.type === "select") {
    wrapper.innerHTML = `
      <label for="${field.path}">${field.label}</label>
      <select id="${field.path}" data-path="${field.path}" data-rerender="${field.rerender ? "true" : "false"}" ${field.required ? "required" : ""}>
        <option value="">Select ${field.label.toLowerCase()}</option>
        ${options.map((option) => `<option value="${option}" ${option === value ? "selected" : ""}>${option}</option>`).join("")}
      </select>
    `;
  } else if (field.type === "textarea") {
    wrapper.innerHTML = `
      <label for="${field.path}">${field.label}</label>
      <textarea class="search-input" id="${field.path}" data-path="${field.path}" rows="5" placeholder="${field.placeholder || ""}">${value}</textarea>
    `;
  } else {
    wrapper.innerHTML = `
      <label for="${field.path}">${field.label}</label>
      <input id="${field.path}" data-path="${field.path}" type="${field.type}" min="${field.min ?? ""}" max="${field.max ?? ""}" step="${field.step ?? ""}" value="${value}" placeholder="${field.placeholder || ""}" ${field.required ? "required" : ""} />
    `;
  }

  bindInputs(wrapper);
  return wrapper;
}

function renderMarks(field) {
  const wrapper = document.createElement("section");
  wrapper.className = "dynamic-group";
  const subjects = getSubjects(field);

  if (!subjects.length) {
    wrapper.innerHTML = `<p class="dynamic-group-title">${field.label}</p><div class="empty-state">Select first.</div>`;
    return wrapper;
  }

  wrapper.innerHTML = `
    <p class="dynamic-group-title">${field.label}</p>
    <div class="marks-grid">
      ${subjects
        .map((subject) => {
          const path = `${field.path}.${subject}`;
          const value = getNested(path) ?? "";
          return `
            <div class="input-group">
              <label for="${path}">${subject}</label>
              <input id="${path}" data-path="${path}" type="number" min="0" max="100" step="1" value="${value}" required />
            </div>
          `;
        })
        .join("")}
    </div>
  `;
  bindInputs(wrapper);
  return wrapper;
}

function renderRatings(field) {
  const wrapper = document.createElement("section");
  wrapper.className = "dynamic-group";
  wrapper.innerHTML = `
    <p class="dynamic-group-title">${field.label}</p>
    <div class="ratings-grid">
      ${field.items
        .map((item) => {
          const path = `${field.path}.${item}`;
          const value = getNested(path) || 3;
          setNested(path, value);
          return `
            <div class="rating-card">
              <label for="${path}">${item}</label>
              <input id="${path}" data-path="${path}" data-rating-label="${path}-value" type="range" min="1" max="5" step="1" value="${value}" />
              <span class="rating-value" id="${path}-value">${value}/5</span>
            </div>
          `;
        })
        .join("")}
    </div>
  `;
  bindInputs(wrapper);
  return wrapper;
}

function renderChips(field) {
  const wrapper = document.createElement("section");
  wrapper.className = "chip-section field-wide";
  const options = getOptions(field);
  const selected = ensureArray(field.path);
  const searchKey = `${activeLevelKey}.${field.path}`;
  const query = chipSearch[searchKey] || "";
  const filtered = options.filter((option) => option.toLowerCase().includes(query.toLowerCase()));

  wrapper.innerHTML = `
    <div class="chip-section-header">
      <div>
        <h3>${field.label}</h3>
        <span class="chip-count">${selected.length} selected</span>
      </div>
      <input class="search-input" type="search" value="${query}" placeholder="Search ${field.label.toLowerCase()}" data-chip-search="${searchKey}" />
    </div>
    <div class="chip-grid">
      ${
        filtered.length
          ? filtered
              .map((option) => {
                const isSelected = selected.includes(option);
                return `<button class="choice-chip ${isSelected ? "selected" : ""}" type="button" data-chip-path="${field.path}" data-chip-value="${option}" aria-pressed="${isSelected}">${option}</button>`;
              })
              .join("")
          : '<span class="chip-empty">No matches.</span>'
      }
    </div>
  `;

  wrapper.querySelector("[data-chip-search]").addEventListener("input", (event) => {
    chipSearch[searchKey] = event.target.value;
    renderAll();
  });

  wrapper.querySelectorAll("[data-chip-path]").forEach((button) => {
    button.addEventListener("click", () => {
      toggleChip(button.dataset.chipPath, button.dataset.chipValue);
      renderAll();
    });
  });

  return wrapper;
}

function renderFile(field) {
  const wrapper = document.createElement("section");
  wrapper.className = "dynamic-group";
  const value = getNested(field.path) || {};
  wrapper.innerHTML = `
    <p class="dynamic-group-title">${field.label}</p>
    <label class="file-drop">
      <span>${value.file_name ? value.file_name : "Upload resume file"}</span>
      <input type="file" accept="${field.accept || ""}" data-file-path="${field.path}" ${field.required ? "required" : ""} />
      <p class="file-note">PDF, DOC, or DOCX.</p>
    </label>
  `;

  wrapper.querySelector("[data-file-path]").addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      setNested(field.path, {
        file_name: file.name,
        file_size: file.size,
        file_type: file.type || "unknown",
      });
      renderAll();
    }
  });

  return wrapper;
}

function bindInputs(root) {
  root.querySelectorAll("[data-path]").forEach((input) => {
    const eventName = input.tagName === "SELECT" ? "change" : "input";
    input.addEventListener(eventName, () => {
      const value = input.type === "number" || input.type === "range" ? input.value : input.value.trim();
      setNested(input.dataset.path, value);

      if (input.dataset.ratingLabel) {
        document.getElementById(input.dataset.ratingLabel).textContent = `${input.value}/5`;
      }

      if (input.dataset.rerender === "true") {
        normalizeDependentState(input.dataset.path);
        renderAll();
      }
    });
  });
}

function toggleChip(path, value) {
  const current = ensureArray(path);
  if (current.includes(value)) {
    setNested(path, current.filter((item) => item !== value));
  } else {
    setNested(path, [...current, value]);
  }
}

function validateField(field) {
  if (field.type === "marks") {
    const subjects = getSubjects(field);
    if (!subjects.length) {
      return `Select the related stream or branch before entering ${field.label.toLowerCase()}.`;
    }
    const missing = subjects.find((subject) => {
      const value = getNested(`${field.path}.${subject}`);
      return value === undefined || value === "" || Number(value) < 0 || Number(value) > 100;
    });
    return missing ? `Enter valid marks for ${missing}.` : "";
  }

  if (field.type === "ratings") {
    const missing = field.items.find((item) => !getNested(`${field.path}.${item}`));
    return missing ? `Rate ${missing}.` : "";
  }

  if (field.type === "chips" && field.required && ensureArray(field.path).length === 0) {
    return `Select at least one ${field.label.toLowerCase()} option.`;
  }

  if (field.type === "file" && field.required && !getNested(field.path)?.file_name) {
    return `${field.label} is required.`;
  }

  if (field.required) {
    const value = getNested(field.path);
    if (value === undefined || value === null || String(value).trim() === "") {
      return `${field.label} is required.`;
    }
    if (field.type === "number" && (Number(value) < Number(field.min ?? -Infinity) || Number(value) > Number(field.max ?? Infinity))) {
      return `${field.label} must be within the allowed range.`;
    }
  }

  return "";
}

function validateStep(step) {
  for (const field of step.fields) {
    const error = validateField(field);
    if (error) {
      return error;
    }
  }
  return "";
}

function validateAllSteps(schema) {
  for (const step of schema.steps) {
    const error = validateStep(step);
    if (error) {
      return error;
    }
  }
  return "";
}

function handleLevelChange() {
  activeLevelKey = levelKeyFromLabel(elements.academicLevel.value);
  currentStep = 0;
  formData = defaultDataFor(activeLevelKey);
  chipSearch = {};
  setMessage("");
  renderAll();
}

function goNext() {
  const schema = schemas[activeLevelKey];
  if (!schema) {
    setMessage("Select your academic level first.", "error");
    return;
  }

  const error = validateStep(schema.steps[currentStep]);
  if (error) {
    setMessage(error, "error");
    return;
  }

  setMessage("");
  currentStep = Math.min(currentStep + 1, schema.steps.length - 1);
  renderAll();
}

function goPrev() {
  setMessage("");
  currentStep = Math.max(currentStep - 1, 0);
  renderAll();
}

async function submitAssessment(event) {
  event.preventDefault();
  setMessage("");

  const schema = schemas[activeLevelKey];
  if (!schema) {
    setMessage("Select your academic level first.", "error");
    return;
  }

  const validationError = validateAllSteps(schema);
  if (validationError) {
    setMessage(validationError, "error");
    return;
  }

  elements.submitButton.disabled = true;
  elements.loadingState.classList.remove("hidden");

  try {
    const response = await fetch("/assessment", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: session.user.id,
        academic_level: schema.label,
        data: formData,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(getApiError(data));
    }

    localStorage.setItem(
      "career_results",
      JSON.stringify({
        ...data,
        user_id: session.user.id,
        generatedAt: new Date().toISOString(),
      })
    );

    setMessage("Recommendations generated. Opening results...", "success");
    window.location.href = "/results";
  } catch (error) {
    setMessage(error.message, "error");
  } finally {
    elements.submitButton.disabled = false;
    elements.loadingState.classList.add("hidden");
  }
}

function logout() {
  localStorage.removeItem("career_session");
  localStorage.removeItem("career_results");
  window.location.href = "/login";
}

const activeSession = requireSession();
if (activeSession) {
  document.getElementById("topbarName").textContent = activeSession.user.full_name;
  document.getElementById("avatarInitials").textContent = initials(activeSession.user.full_name);
  const mappedLevel = levelAliases[activeSession.user.academic_level] || "";
  elements.academicLevel.value = mappedLevel;
  activeLevelKey = levelKeyFromLabel(mappedLevel);
  formData = defaultDataFor(activeLevelKey);
  document.getElementById("logoutButton").addEventListener("click", logout);
  elements.academicLevel.addEventListener("change", handleLevelChange);
  elements.prevButton.addEventListener("click", goPrev);
  elements.nextButton.addEventListener("click", goNext);
  elements.form.addEventListener("submit", submitAssessment);
  renderAll();
}
