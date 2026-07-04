import pytest

from yasbd import BoundaryDetector, register_lang_packs

# Register self
register_lang_packs(["yasbd_union"])


TEST_DATA = [
    # Basic sentences (Mixed language)
    "Hello world!| How are you?| I'm fine.",
    "ሰላም ሁሉም ሰው።| ደህና ነህ?| ደህና ነኝ።",
    "你好世界。| 你好吗？| 我很好。",
    "信じられない！| 本当にそうなの？| 早く教えてください。",
    "ครับ| สบายดีไหม| สบายดี",
    "เวลา 08.30 น. เริ่มเรียน เลิก 16.00 น.",
    "我喜欢AI。|It is useful",
    "Ｕ．Ｓ．Ａ．的经济政策非常复杂。|下个月的动向值得关注。",
    "那个会议在下午两点。|Please don't be late!",
    # Abbreviations
    "Prof. Smith und Dr. Schmidt arbeiten zusammen.| Das Projekt ist groß.",
    "डॉ. सिंह और प्रो. वर्मा ने व्याख्यान दिया।| उन्होंने भौतिकी पढ़ाई।",
    "D. José y Dña. María son los dueños.| El Cmdte. Rodríguez saludó al Cnel. Díaz.",
    "Это, т.е. новый закон, вступает в силу.| Встреча назначена на пн. 15 января.",
    "Η συνάντηση είναι τη Δευ. 15 Ιαν.| Γεννήθηκε στις 5 Μαρ. 1990.",
    "Το μάθημα είναι Τετ. και Παρ. κάθε εβδομάδα.",
    "The U.S. Army is recruiting.| Many join every year.",
    "She lived in the U.S.A. for 20 years.| Now she lives in the E.U.",
    "ዶ/ር ኃይሉ በሆስፒታሉ ውስጥ ናቸው።| ነገ ይመረመራሉ።",
    "Das ist z. B. ein Beispiel.| Es funktioniert gut.",
    # Quoted speech
    "Er sagte: 'Ich bin müde.'| Dann ging er nach Hause.",
    "„Das ist großartig!“ rief sie.",
    "Léa dit : « Bonjour ! Je suis Léa. Et toi ? »",
    "Elle s'est tournée vers lui, \"C'est magnifique.\" dit-elle.",
    # Ellipsis
    "Die Ergebnisse waren nicht eindeutig....| Wir haben es wiederholt.",
    "Het project was bijna afgerond... of dat dachten we tenminste.",
]


@pytest.mark.parametrize("test_case", TEST_DATA)
def test_segmentation(subtests, test_case):
    """Test sentence segmentation for xx multilingual aggregate."""
    expected = [sent.strip() for sent in test_case.split("|")]
    input_text = test_case.replace("|", "")

    seg = BoundaryDetector(lang="xx")
    result = list(seg.segment(input_text))

    assert result == expected, f"Input: {input_text}"
