package com.rafiul.ai_banglish_keyboardapp

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONArray
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class AIConverter(private val context: Context) {

    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    companion object {
        private const val API_URL = "https://api.groq.com/openai/v1/chat/completions"
        private const val MODEL   = "llama-3.3-70b-versatile"
        private const val SYSTEM  = """You are a Banglish converter for Bangladeshi users.
Banglish = Bengali written in Roman/English script mixed with English words.
RULES:
- Preserve meaning and tone exactly
- For bangla: return proper Unicode Bengali ONLY
- For english: return natural grammatically correct English
- Return ONLY converted text, nothing else
EXAMPLES:
"ami tired, ghume jabo" → বাংলা: "আমি ক্লান্ত, ঘুমাতে যাবো"
"bhai kemon acho" → English: "Bro how are you"
"""
    }

    suspend fun convert(text: String, toBangla: Boolean): Result<String> {
        return withContext(Dispatchers.IO) {
            try {
                val apiKey = getApiKey()
                if (apiKey.isEmpty()) return@withContext Result.failure(
                    Exception("API Key not set!\nGo to Settings → enter your Groq key.")
                )

                val target  = if (toBangla) "বাংলা (Bengali Unicode)" else "English"
                val userMsg = "Convert to $target:\n\n${text.trim()}"

                val body = JSONObject().apply {
                    put("model", MODEL)
                    put("max_tokens", 1000)
                    put("messages", JSONArray().apply {
                        put(JSONObject().apply { put("role","system"); put("content", SYSTEM) })
                        put(JSONObject().apply { put("role","user");   put("content", userMsg) })
                    })
                }.toString()

                val req = Request.Builder()
                    .url(API_URL)
                    .addHeader("Authorization", "Bearer $apiKey")
                    .addHeader("Content-Type", "application/json")
                    .post(body.toRequestBody("application/json".toMediaType()))
                    .build()

                val res = client.newCall(req).execute()
                if (!res.isSuccessful) return@withContext Result.failure(
                    Exception(when(res.code) {
                        401  -> "Invalid API key. Go to Settings and check."
                        429  -> "Rate limit reached. Wait a moment."
                        else -> "API error ${res.code}"
                    })
                )

                val text2 = JSONObject(res.body!!.string())
                    .getJSONArray("choices")
                    .getJSONObject(0)
                    .getJSONObject("message")
                    .getString("content").trim()

                Result.success(text2)

            } catch (e: Exception) {
                Result.failure(Exception("Error: ${e.message?.take(60)}"))
            }
        }
    }

    private fun getApiKey() = context
        .getSharedPreferences("banglish_prefs", Context.MODE_PRIVATE)
        .getString("api_key", "") ?: ""
}
