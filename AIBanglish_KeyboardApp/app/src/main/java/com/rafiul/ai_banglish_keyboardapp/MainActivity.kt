package com.rafiul.ai_banglish_keyboardapp

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.rafiul.ai_banglish_keyboardapp.databinding.ActivityMainBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var converter: AIConverter
    private var lastResult = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        converter = AIConverter(this)
        setupButtons()
    }

    private fun setupButtons() {

        // AI → বাংলা
        binding.btnToBangla.setOnClickListener {
            convert(toBangla = true)
        }

        // AI → English
        binding.btnToEnglish.setOnClickListener {
            convert(toBangla = false)
        }

        // Copy
        binding.btnCopy.setOnClickListener {
            if (lastResult.isEmpty()) {
                toast("Nothing to copy yet!")
                return@setOnClickListener
            }
            val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
            clipboard.setPrimaryClip(ClipData.newPlainText("Converted", lastResult))
            toast("✅ Copied!")
        }

        // Share
        binding.btnShare.setOnClickListener {
            if (lastResult.isEmpty()) {
                toast("Nothing to share yet!")
                return@setOnClickListener
            }
            startActivity(Intent.createChooser(
                Intent(Intent.ACTION_SEND).apply {
                    type = "text/plain"
                    putExtra(Intent.EXTRA_TEXT, lastResult)
                }, "Share via"
            ))
        }

        // Clear
        binding.btnClear.setOnClickListener {
            binding.etInput.setText("")
            binding.tvOutput.text = ""
            binding.tvStatus.text = ""
            lastResult = ""
        }

        // Settings
        binding.btnSettings.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }
    }

    private fun convert(toBangla: Boolean) {
        val input = binding.etInput.text.toString().trim()
        if (input.isEmpty()) {
            toast("Please type something first!")
            return
        }

        val label = if (toBangla) "বাংলা" else "English"
        setLoading(true, "⏳ Converting to $label...")

        CoroutineScope(Dispatchers.Main).launch {
            val result = withContext(Dispatchers.IO) {
                converter.convert(input, toBangla)
            }

            setLoading(false, "")

            result.onSuccess { converted ->
                lastResult = converted
                binding.tvOutput.text = converted
                binding.tvStatus.text = "✅ Converted to $label!"
                binding.tvStatus.setTextColor(0xFF4CAF50.toInt())
            }

            result.onFailure { error ->
                binding.tvStatus.text = "❌ ${error.message}"
                binding.tvStatus.setTextColor(0xFFF44336.toInt())
            }
        }
    }

    private fun setLoading(loading: Boolean, msg: String) {
        binding.btnToBangla.isEnabled  = !loading
        binding.btnToEnglish.isEnabled = !loading
        binding.tvStatus.text          = msg
        binding.tvStatus.setTextColor(0xFF6C7086.toInt())
    }

    private fun toast(msg: String) =
        Toast.makeText(this, msg, Toast.LENGTH_SHORT).show()
}
