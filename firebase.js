// firebase.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getDatabase } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-database.js";

// 🔹 Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyCkWKmK_UmQtk6UEIset5e6iPmFZj0ZLHc",
  authDomain: "bugemtoolsdb.firebaseapp.com",
  databaseURL: "https://bugemtoolsdb-default-rtdb.firebaseio.com",
  projectId: "bugemtoolsdb",
  storageBucket: "bugemtoolsdb.firebasestorage.app",
  messagingSenderId: "52270788635",
  appId: "1:52270788635:web:59bf1c23406beb872e48be",
  measurementId: "G-SHMYMXM4Z4"
};

// 🔹 Inisialisasi Firebase
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// 🔹 Export supaya bisa dipakai di semua file HTML
export { app, db };