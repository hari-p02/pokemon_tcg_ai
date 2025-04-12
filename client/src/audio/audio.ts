// Imports
import axios from 'axios';

// Define KiwiAudioData interface locally since we can't import it
interface PokemonAudioData {
  audioKey: string;
  durationSeconds: number;
  isReady: boolean;
  generateFailed: boolean;
}

enum ElevenLabsModelId {
  Turbo = 'eleven_turbo_v2',
}

type AudioCompletionCallback = (audioKey: string) => void;
const audioCompletionCallbacks = new Set<AudioCompletionCallback>();

/**
 * Subscribe to audio generation completion events
 * @param callback - Function to be called when audio generation completes
 * @returns Function to unsubscribe
 */
export function subscribeToAudioCompletion(
  callback: AudioCompletionCallback
): () => void {
  audioCompletionCallbacks.add(callback);
  return () => audioCompletionCallbacks.delete(callback);
}

// Main entry point function
export function generateAudio(
  text: string,
  voiceId: string,
  fallbackDurationSeconds: number
): PokemonAudioData {
  const audioKey = createAudioKey(text, voiceId);

  const audioData: PokemonAudioData = {
    audioKey,
    durationSeconds: fallbackDurationSeconds,
    isReady: false,
    generateFailed: false,
  };

  generateNewAudio(audioData, text, voiceId, fallbackDurationSeconds, () => {
    audioCompletionCallbacks.forEach((callback) => callback(audioKey));
  }).catch((error) => {
    console.error('Failed to generate audio:', error);
    audioData.generateFailed = true;
  });

  return audioData;
}

async function generateNewAudio(
  audioData: PokemonAudioData,
  text: string,
  voiceId: string,
  fallbackDurationSeconds: number,
  onComplete?: () => void
): Promise<void> {
  console.info('Generating new audio via ElevenLabs. key:', audioData.audioKey);

  /**************************
   * Generate new audio via ElevenLabs
   **************************/
  try {
    // Making API call to ElevenLabs directly
    const response = await axios.post(
      `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`,
      {
        text,
        model_id: ElevenLabsModelId.Turbo,
        output_format: 'mp3',
      },
      {
        headers: {
          'Content-Type': 'application/json',
          'xi-api-key': import.meta.env.VITE_ELEVENLABS_API_KEY,
        },
        responseType: 'arraybuffer',
      }
    );

    // For direct binary response, we won't have alignment data
    // Just use the fallback duration
    console.log('Successfully received audio data from ElevenLabs');

    audioData.durationSeconds = fallbackDurationSeconds;
    audioData.isReady = true;
    onComplete?.();
  } catch (error) {
    console.error('Failed to generate audio via ElevenLabs:', error);
    audioData.generateFailed = true;
    onComplete?.();
    return;
  }
}

// Helper to create deterministic audio key
function createAudioKey(text: string, voiceId: string): string {
  const normalizedText = text.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  const encodedText = btoa(unescape(encodeURIComponent(normalizedText)));
  return `pokemon/${voiceId}/cards/${encodedText}.mp3`;
}
