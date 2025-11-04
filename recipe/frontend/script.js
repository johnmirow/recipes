let currentLang = "en";
const savedLang = localStorage.getItem("language");
if (savedLang) {
  currentLang = savedLang;
} else {
  const browserLang = navigator.language.toLowerCase();
  if (browserLang.startsWith("sk") || browserLang.startsWith("cs")) currentLang = "sk";
  else currentLang = "en";
  localStorage.setItem("language", currentLang);
}

const translations = {
  en: {
    title: "🥗 Food Allergy Recipes",
    loginHeader: "Login",
    email: "Email",
    password: "Password",
    loginButton: "Login",
    addHeader: "Add New Recipe",
    titleInput: "Title",
    descriptionInput: "Description",
    instructionsInput: "Instructions",
    addButton: "Add Recipe",
    searchHeader: "Search Safe Recipes",
    excludePlaceholder: "Allergens to avoid (comma separated)",
    searchButton: "Search",
    resultsHeader: "Results",
    noResults: "No safe recipes found.",
    statusRecipeAdded: "✅ Recipe added successfully!",
    statusRecipeFail: "❌ Failed to add recipe.",
    statusLoginSuccess: "✅ Login successful!",
    statusLoginFail: "❌ Invalid email or password.",
    imagePlaceholder: "Image URL (optional)",
    sourcePlaceholder: "Source URL (YouTube/Instagram/blog)",
    myHeader: "My Recipes",
    myButton: "Load My Recipes",
    invalidImage: "⚠️ Invalid image URL.",
    invalidSource: "⚠️ Invalid source URL.",
    apiError: "❌ A network error occurred. Please try again."
  },
  sk: {
    title: "🥗 Recepty bez alergénov",
    loginHeader: "Prihlásenie",
    email: "E-mail",
    password: "Heslo",
    loginButton: "Prihlásiť",
    addHeader: "Pridať nový recept",
    titleInput: "Názov receptu",
    descriptionInput: "Popis",
    instructionsInput: "Postup",
    addButton: "Pridať recept",
    searchHeader: "Vyhľadať bezpečné recepty",
    excludePlaceholder: "Alergény na vynechanie (oddelené čiarkou)",
    searchButton: "Hľadať",
    resultsHeader: "Výsledky",
    noResults: "Neboli nájdené žiadne bezpečné recepty.",
    statusRecipeAdded: "✅ Recept bol úspešne pridaný!",
    statusRecipeFail: "❌ Nepodarilo sa pridať recept.",
    statusLoginSuccess: "✅ Prihlásenie úspešné!",
    statusLoginFail: "❌ Nesprávny e-mail alebo heslo.",
    imagePlaceholder: "URL obrázka (voliteľné)",
    sourcePlaceholder: "Zdrojový odkaz (YouTube/Instagram/blog)",
    myHeader: "Moje recepty",
    myButton: "Načítať moje recepty",
    invalidImage: "⚠️ Neplatná adresa obrázka.",
    invalidSource: "⚠️ Neplatná adresa zdroja.",
    apiError: "❌ Nastala sieťová chyba. Skúste znova."
  }
};

const API_URL = "http://127.0.0.1:8000";
let token = null;

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("language", lang);
  const t = translations[lang];
  document.title = t.title;
  document.querySelector("h1").textContent = t.title;
  document.querySelector("#login h2").textContent = t.loginHeader;
  document.getElementById("email").placeholder = t.email;
  document.getElementById("password").placeholder = t.password;
  document.querySelector("#login button").textContent = t.loginButton;
  document.querySelector("#addRecipe h2").textContent = t.addHeader;
  document.getElementById("title").placeholder = t.titleInput;
  document.getElementById("description").placeholder = t.descriptionInput;
  document.getElementById("instructions").placeholder = t.instructionsInput;
  document.getElementById("image_url").placeholder = t.imagePlaceholder;
  document.getElementById("source_url").placeholder = t.sourcePlaceholder;
  document.querySelector("#search h2").textContent = t.searchHeader;
  document.getElementById("exclude").placeholder = t.excludePlaceholder;
  document.getElementById("btnSearch").textContent = t.searchButton;
  document.querySelector("#results h2").textContent = t.resultsHeader;
  document.querySelector("#myHeader").textContent = t.myHeader;
  document.getElementById("btnLoadMine").textContent = t.myButton;
  document.querySelectorAll("#lang-switch button").forEach(btn => {
    btn.classList.toggle("active", btn.textContent.toLowerCase().startsWith(lang));
  });
}

function isValidHttpUrl(str) {
  if (!str) return true; // optional field
  try {
    const u = new URL(str);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch { return false; }
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const status = document.getElementById("loginStatus");

  try {
    const res = await fetch(`${API_URL}/users/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (res.ok) {
      const data = await res.json();
      token = data.access_token;
      status.textContent = translations[currentLang].statusLoginSuccess;
      document.getElementById("addRecipe").style.display = "block";
      document.getElementById("myRecipes").style.display = "block";
    } else {
      status.textContent = translations[currentLang].statusLoginFail;
    }
  } catch (e) {
    status.textContent = translations[currentLang].apiError;
  }
}

async function addRecipe() {
  const t = translations[currentLang];
  const source = document.getElementById("source_url").value.trim();
  const image = document.getElementById("image_url").value.trim();
  const status = document.getElementById("recipeStatus");

  if (!isValidHttpUrl(source)) { status.textContent = t.invalidSource; return; }
  if (!isValidHttpUrl(image)) { status.textContent = t.invalidImage; return; }

  const recipe = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    instructions: document.getElementById("instructions").value,
    prep_time: parseInt(document.getElementById("prep_time").value) || null,
    cook_time: parseInt(document.getElementById("cook_time").value) || null,
    servings: parseInt(document.getElementById("servings").value) || null,
    source_url: source || null,
    image_url: image || null
  };

  try {
    const res = await fetch(`${API_URL}/recipes/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify(recipe)
    });
    status.textContent = res.ok ? t.statusRecipeAdded : t.statusRecipeFail;
  } catch (e) {
    status.textContent = t.apiError;
  }
}

function sourceBadge(url) {
  if (!url) return "";
  try {
    const host = new URL(url).hostname.toLowerCase();
    if (host.includes("youtube") || host.includes("youtu.be")) return "▶️";
    if (host.includes("instagram")) return "📸";
    if (host.includes("tiktok")) return "🎵";
    if (host.includes("facebook")) return "📘";
    if (host.includes("pinterest")) return "📌";
    return "🌐";
  } catch { return "🌐"; }
}

function renderRecipeLI(r) {
  const li = document.createElement("li");
  li.className = "list-item";

  const img = document.createElement("img");
  img.className = "thumb";
  img.alt = "recipe image";
  img.src = r.image_url || "images/placeholder.svg";
  img.onerror = () => { img.onerror = null; img.src = "images/placeholder.svg"; };
  li.appendChild(img);

  const titleText = `${r.title} (ID: ${r.recipe_id})`;
  const badge = document.createElement("span");
  badge.className = "badge";
  badge.textContent = sourceBadge(r.source_url);

  if (r.source_url) {
    const a = document.createElement("a");
    a.href = r.source_url;
    a.target = "_blank";
    a.rel = "noopener";
    a.className = "title-link";
    a.textContent = titleText;
    li.appendChild(a);
  } else {
    const span = document.createElement("span");
    span.textContent = titleText;
    li.appendChild(span);
  }
  li.appendChild(badge);
  return li;
}

async function searchRecipes() {
  const t = translations[currentLang];
  const exclude = document.getElementById("exclude").value
    .split(",")
    .map(s => s.trim())
    .filter(Boolean);

  const params = new URLSearchParams();
  exclude.forEach(a => params.append("exclude", a));

  const list = document.getElementById("recipeList");
  list.innerHTML = "";

  try {
    const res = await fetch(`${API_URL}/search/safe?${params.toString()}`);
    if (!res.ok) throw new Error();
    const data = await res.json();

    if (data.length === 0) {
      list.innerHTML = `<li>${t.noResults}</li>`;
      return;
    }

    // Fetch full recipes to map URLs for thumbnails/links
    const resAll = await fetch(`${API_URL}/recipes/`);
    if (!resAll.ok) throw new Error();
    const full = await resAll.json();

    data.forEach(sr => {
      const r = full.find(item => item.recipe_id === sr.recipe_id) || { title: sr.title, recipe_id: sr.recipe_id };
      list.appendChild(renderRecipeLI(r));
    });
  } catch (e) {
    list.innerHTML = `<li class="error">${t.apiError}</li>`;
  }
}

async function loadMyRecipes() {
  const t = translations[currentLang];
  const list = document.getElementById("myList");
  list.innerHTML = "";
  try {
    const res = await fetch(`${API_URL}/recipes/me`, {
      headers: { "Authorization": `Bearer ${token}` }
    });
    if (!res.ok) throw new Error();
    const data = await res.json();
    if (data.length === 0) {
      list.innerHTML = "<li>No recipes yet.</li>";
      return;
    }
    data.forEach(r => list.appendChild(renderRecipeLI(r)));
  } catch (e) {
    list.innerHTML = `<li class="error">${t.apiError}</li>`;
  }
}

window.addEventListener("DOMContentLoaded", () => setLanguage(currentLang));
