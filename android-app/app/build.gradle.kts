plugins {
    id("com.android.application")
}

android {
    namespace = "com.pbai.jarvis"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.pbai.jarvis"
        minSdk = 23
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
