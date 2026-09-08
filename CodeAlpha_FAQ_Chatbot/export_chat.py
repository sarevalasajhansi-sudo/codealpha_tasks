from datetime import datetime


def export_as_txt(chat_history, filename):
    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("AI & Technology FAQ Chatbot\n")
        file.write("=" * 60 + "\n")
        file.write(
            f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        for item in chat_history:

            file.write(
                f"[{item['time']}]\n"
            )

            file.write(
                f"You: {item['user']}\n"
            )

            file.write(
                f"Bot: {item['bot']}\n"
            )

            file.write(
                f"Similarity: {item['confidence']}%\n"
            )

            file.write(
                "-" * 60 + "\n\n"
            )


def export_as_pdf(chat_history, filename):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer
    )

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    normal_style = styles["BodyText"]

    content = []

    content.append(
        Paragraph(
            "AI & Technology FAQ Chatbot",
            title_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            normal_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    for item in chat_history:

        content.append(
            Paragraph(
                f"<b>[{item['time']}]</b>",
                normal_style
            )
        )

        content.append(
            Paragraph(
                f"<b>You:</b> {item['user']}",
                normal_style
            )
        )

        bot_text = item["bot"].replace(
            "\n",
            "<br/>"
        )

        content.append(
            Paragraph(
                f"<b>Bot:</b> {bot_text}",
                normal_style
            )
        )

        content.append(
            Paragraph(
                f"Similarity: {item['confidence']}%",
                normal_style
            )
        )

        content.append(
            Spacer(1, 12)
        )

    document.build(content)