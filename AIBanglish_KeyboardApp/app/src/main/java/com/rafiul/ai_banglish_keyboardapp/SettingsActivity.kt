package com.rafiul.ai_banglish_keyboardapp

import android.content.Context
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.rafiul.ai_banglish_keyboardapp.databinding.ActivitySettingsBinding

class SettingsActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySettingsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySettingsBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // Load saved key
        binding.etApiKey.setText(loadKey())

        binding.btnSave.setOnClickListener {
            val key = binding.etApiKey.text.toString().trim()
            if (key.isEmpty()) {
                binding.tvStatus.text = "⚠️ Key cannot be empty!"
                binding.tvStatus.setTextColor(0xFFF44336.toInt())
                return@setOnClickListener
            }
            saveKey(key)
            binding.tvStatus.text = "✅ Saved!"
            binding.tvStatus.setTextColor(0xFF4CAF50.toInt())
        }
    }

    private fun saveKey(key: String) {
        getSharedPreferences("banglish_prefs", Context.MODE_PRIVATE)
            .edit().putString("api_key", key).apply()
    }

    private fun loadKey(): String {
        return getSharedPreferences("banglish_prefs", Context.MODE_PRIVATE)
            .getString("api_key", "") ?: ""
    }
}
