import os
import textwrap

def generate_multi_subtitles( text="A majestic lioness stands proudly, scanning the horizon across the vast savanna.", line_duration=2,
    max_width=40, output_srt="output/subtitles.srt"):
    """
    Splits 'text' into multiple lines (up to 'max_width' characters each),
    then generates an .srt file where each line is shown for 'line_duration' seconds.
    This creates a "stepped" or "gradual reveal" effect in standard SRT subtitles.
    """

    # making sure that the output folder exists
    os.makedirs(os.path.dirname(output_srt), exist_ok=True)

    # Wrapping the text so no single line is too wide
    wrapped_lines = textwrap.wrap(text, width=max_width)

    # accumulating the SRT content here
    srt_content = []
    current_start_second = 0

    for i, line_text in enumerate(wrapped_lines, start=1):
        # Start time
        start_sec = current_start_second
        # End time = start + line_duration
        end_sec = current_start_second + line_duration

        # Converting seconds to SRT time format "HH:MM:SS,mmm"
        start_time_str = f"00:00:{start_sec:02d},000"
        end_time_str   = f"00:00:{end_sec:02d},000"

        srt_content.append(
            f"{i}\n"
            f"{start_time_str} --> {end_time_str}\n"
            f"{line_text}\n\n"
        )

        current_start_second += line_duration

    with open(output_srt, "w", encoding="utf-8") as f:
        f.writelines(srt_content)

    print(f"Multi-subtitle file generated: {output_srt}")
    return output_srt

if __name__ == "__main__":
    # Example usage:
    generate_multi_subtitles(
        text="A majestic lioness stands proudly, scanning the horizon across the vast savanna.",
        line_duration=2,
        max_width=40,
        output_srt="output/subtitles.srt"
    )
