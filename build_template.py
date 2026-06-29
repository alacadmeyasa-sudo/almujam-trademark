# -*- coding: utf-8 -*-
"""
Generator for the Elementor landing-page template.
Service: تظلم من رفض العلامة التجارية
Primary keyword: تظلم رفض العلامة التجارية
Contact number: 966541447701

Running this script regenerates `elementor-template.json`.
Every node carries a stable, unique Elementor id and standard widget
settings, so the imported page is fully editable element-by-element
inside the Elementor editor.
"""
import json
import os
import random
import string

# ---------------------------------------------------------------------------
# Brand / contact constants (edit here, then re-run to regenerate the JSON)
# ---------------------------------------------------------------------------
PHONE_RAW = "966541447701"           # used for tel: and wa.me links
PHONE_DISPLAY = "‏+966 54 144 7701"   # shown to visitors (RTL-safe)
PRIMARY_KEYWORD = "تظلم رفض العلامة التجارية"
SERVICE_NAME = "تظلم من رفض العلامة التجارية"

TEL_LINK = "tel:+%s" % PHONE_RAW
WA_LINK = "https://wa.me/%s?text=%s" % (
    PHONE_RAW,
    "أرغب%20في%20تقديم%20تظلم%20على%20رفض%20علامتي%20التجارية",
)

# Brand colors
NAVY = "#0B1F3A"
GOLD = "#C8A24B"
GOLD_DARK = "#A9863A"
LIGHT = "#F5F7FA"
WHITE = "#FFFFFF"
GREY = "#5A6473"

random.seed(20260629)  # deterministic ids across regenerations


def uid():
    return "".join(random.choice("abcdef0123456789") for _ in range(7))


# ---------------------------------------------------------------------------
# Low-level Elementor builders
# ---------------------------------------------------------------------------
def section(elements, settings=None):
    return {
        "id": uid(),
        "elType": "section",
        "settings": settings or {},
        "elements": elements,
        "isInner": False,
    }


def inner_section(elements, settings=None):
    return {
        "id": uid(),
        "elType": "section",
        "settings": settings or {},
        "elements": elements,
        "isInner": True,
    }


def column(elements, size=100, settings=None):
    base = {"_column_size": size, "_inline_size": None}
    if settings:
        base.update(settings)
    return {
        "id": uid(),
        "elType": "column",
        "settings": base,
        "elements": elements,
        "isInner": False,
    }


def widget(widget_type, settings):
    return {
        "id": uid(),
        "elType": "widget",
        "settings": settings,
        "elements": [],
        "widgetType": widget_type,
    }


# ---------------------------------------------------------------------------
# Widget helpers (Arabic / RTL aware)
# ---------------------------------------------------------------------------
def heading(text, tag="h2", color=NAVY, size=None, align="right", extra=None):
    s = {
        "title": text,
        "header_size": tag,
        "align": align,
        "title_color": color,
        "_element_custom_width": {"unit": "%", "size": 100},
    }
    if size:
        s["typography_typography"] = "custom"
        s["typography_font_size"] = {"unit": "px", "size": size, "sizes": []}
        s["typography_font_weight"] = "700"
    if extra:
        s.update(extra)
    return widget("heading", s)


def text_editor(html, align="right", color=GREY):
    return widget(
        "text-editor",
        {
            "editor": html,
            "align": align,
            "text_color": color,
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 17, "sizes": []},
            "typography_line_height": {"unit": "em", "size": 1.9, "sizes": []},
        },
    )


def button(text, link, color=WHITE, bg=GOLD, align="right", icon="fas fa-phone-alt"):
    return widget(
        "button",
        {
            "text": text,
            "link": {"url": link, "is_external": "true", "nofollow": "", "custom_attributes": ""},
            "align": align,
            "button_text_color": color,
            "background_color": bg,
            "border_radius": {"unit": "px", "top": 10, "right": 10, "bottom": 10, "left": 10, "isLinked": True},
            "text_padding": {"unit": "px", "top": 18, "right": 38, "bottom": 18, "left": 38, "isLinked": False},
            "selected_icon": {"value": icon, "library": "fa-solid"},
            "icon_align": "right",
            "icon_indent": {"unit": "px", "size": 10, "sizes": []},
            "typography_typography": "custom",
            "typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "typography_font_weight": "700",
        },
    )


def icon_box(icon, title, desc, primary=GOLD):
    return widget(
        "icon-box",
        {
            "selected_icon": {"value": icon, "library": "fa-solid"},
            "title_text": title,
            "description_text": desc,
            "position": "top",
            "text_align": "center",
            "title_color": NAVY,
            "description_color": GREY,
            "primary_color": primary,
            "icon_size": {"unit": "px", "size": 38, "sizes": []},
            "icon_space": {"unit": "px", "size": 18, "sizes": []},
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": 21, "sizes": []},
            "title_typography_font_weight": "700",
            "description_typography_typography": "custom",
            "description_typography_font_size": {"unit": "px", "size": 16, "sizes": []},
            "description_typography_line_height": {"unit": "em", "size": 1.8, "sizes": []},
        },
    )


def icon_list(items, color=NAVY):
    return widget(
        "icon-list",
        {
            "icon_list": [
                {
                    "_id": uid(),
                    "text": t,
                    "selected_icon": {"value": "fas fa-check-circle", "library": "fa-solid"},
                }
                for t in items
            ],
            "space_between": {"unit": "px", "size": 14, "sizes": []},
            "icon_color": GOLD,
            "text_color": color,
            "icon_size": {"unit": "px", "size": 20, "sizes": []},
            "text_indent": {"unit": "px", "size": 12, "sizes": []},
            "icon_typography_typography": "custom",
            "icon_typography_font_size": {"unit": "px", "size": 17, "sizes": []},
        },
    )


def spacer(size=40):
    return widget("spacer", {"space": {"unit": "px", "size": size, "sizes": []}})


def divider():
    return widget(
        "divider",
        {"color": GOLD, "weight": {"unit": "px", "size": 3, "sizes": []},
         "width": {"unit": "px", "size": 70, "sizes": []}, "align": "right"},
    )


def accordion(pairs):
    return widget(
        "accordion",
        {
            "tabs": [
                {"_id": uid(), "tab_title": q, "tab_content": a} for q, a in pairs
            ],
            "title_color": NAVY,
            "tab_active_color": GOLD,
            "content_color": GREY,
            "selected_icon": {"value": "fas fa-plus", "library": "fa-solid"},
            "selected_active_icon": {"value": "fas fa-minus", "library": "fa-solid"},
            "title_typography_typography": "custom",
            "title_typography_font_size": {"unit": "px", "size": 18, "sizes": []},
            "title_typography_font_weight": "700",
        },
    )


# ---------------------------------------------------------------------------
# Section settings presets
# ---------------------------------------------------------------------------
def sec_settings(bg=None, gradient=False, pad_top=70, pad_bottom=70, content_width="boxed"):
    s = {
        "layout": content_width,
        "padding": {"unit": "px", "top": pad_top, "right": 0, "bottom": pad_bottom, "left": 0, "isLinked": False},
        "structure": "10",
    }
    if gradient:
        s.update({
            "background_background": "gradient",
            "background_color": NAVY,
            "background_color_b": "#13325c",
            "background_gradient_angle": {"unit": "deg", "size": 135, "sizes": []},
        })
    elif bg:
        s.update({"background_background": "classic", "background_color": bg})
    return s


# ===========================================================================
# Build the page content
# ===========================================================================
content = []

# --- 1. HERO -----------------------------------------------------------------
hero_col = column([
    heading(PRIMARY_KEYWORD, tag="h1", color=WHITE, size=46, align="right"),
    heading("لا تدع رفض إدارة العلامات يوقف مشروعك — نُعد ونقدّم تظلمك باحترافية ونتابعه حتى القبول",
            tag="h3", color=GOLD, size=22, align="right"),
    text_editor(
        "<p>فريق متخصص في <strong>التظلم من رفض العلامة التجارية</strong> أمام الجهات المختصة "
        "بالمملكة العربية السعودية. ندرس أسباب الرفض، ونصيغ مذكرة التظلم النظامية، ونرفقها "
        "بالمستندات والسوابق التي تعزّز قبول علامتك التجارية.</p>",
        color="#D7DEEA"),
    spacer(10),
    inner_section([
        column([button("اتصل الآن — استشارة فورية", TEL_LINK, bg=GOLD, icon="fas fa-phone-alt")], size=50),
        column([button("تواصل عبر واتساب", WA_LINK, bg="#25D366", icon="fab fa-whatsapp")], size=50),
    ], {"gap": "default"}),
    spacer(8),
    text_editor("<p style='font-size:18px;color:#FFFFFF'>📞 %s</p>" % PHONE_DISPLAY, color=WHITE),
])
content.append(section([hero_col], sec_settings(gradient=True, pad_top=110, pad_bottom=110)))

# --- 2. WHAT IS IT -----------------------------------------------------------
about_col = column([
    heading("ما هو التظلم من رفض العلامة التجارية؟", tag="h2", size=34),
    divider(),
    text_editor(
        "<p>عندما تتقدّم بطلب تسجيل علامة تجارية وتصدر إدارة العلامات قرارًا بالرفض، "
        "يمنحك النظام السعودي الحق في تقديم <strong>تظلم على رفض تسجيل العلامة التجارية</strong> "
        "خلال المدة النظامية المحددة. التظلم هو مذكرة قانونية مسبّبة تُوضّح عدم صحة أسباب الرفض "
        "وتطالب بإعادة النظر في القرار وقبول العلامة.</p>"
        "<p>نتولّى عنك إعداد صيغة التظلم من رفض تسجيل علامة تجارية بشكل نظامي دقيق، مدعّمة "
        "بالحجج والمستندات، لرفع فرص قبول علامتك وحماية هويتك التجارية.</p>"),
], 60)
about_side = column([
    icon_list([
        "مهلة نظامية محددة لتقديم التظلم",
        "مذكرة قانونية مسبّبة ومدعّمة بالأدلة",
        "متابعة الطلب حتى صدور القرار النهائي",
        "خبرة في تظلمات العلامات التجارية",
    ]),
], 40)
content.append(section([about_col, about_side], sec_settings(bg=WHITE, content_width="boxed")))

# --- 3. REASONS FOR REJECTION ------------------------------------------------
reasons_head = column([
    heading("أبرز أسباب رفض تسجيل العلامة التجارية", tag="h2", size=32, align="center"),
    text_editor("<p style='text-align:center'>معرفة سبب الرفض هي الخطوة الأولى لبناء تظلم ناجح. "
                "من أكثر الأسباب شيوعًا:</p>", align="center"),
])
content.append(section([reasons_head], sec_settings(bg=LIGHT, pad_bottom=20)))

reasons = [
    ("fas fa-clone", "التشابه مع علامة قائمة", "وجود علامة مسجّلة أو مطلوب تسجيلها تتشابه معها في الاسم أو الشكل."),
    ("fas fa-ban", "مخالفة النظام العام", "احتواء العلامة على ألفاظ أو رموز مخالفة للأنظمة أو الآداب العامة."),
    ("fas fa-font", "الوصفية والعمومية", "كون العلامة وصفًا مباشرًا للمنتج أو لفظًا عامًا لا يميّز نشاطك."),
    ("fas fa-flag", "رموز محظورة", "استخدام أعلام أو شعارات رسمية أو رموز دينية لا يُسمح بتسجيلها."),
    ("fas fa-image", "ضعف العنصر المميّز", "عدم احتواء العلامة على عنصر ابتكاري يميّزها عن غيرها."),
    ("fas fa-file-alt", "نقص المستندات", "قصور في البيانات أو المرفقات المقدّمة مع طلب التسجيل."),
]
r_cols = [column([icon_box(i, t, d)], 33) for (i, t, d) in reasons[:3]]
content.append(section(r_cols, sec_settings(bg=LIGHT, pad_top=20, pad_bottom=20)))
r_cols2 = [column([icon_box(i, t, d)], 33) for (i, t, d) in reasons[3:]]
content.append(section(r_cols2, sec_settings(bg=LIGHT, pad_top=20, pad_bottom=60)))

# --- 4. STEPS ----------------------------------------------------------------
steps_head = column([
    heading("خطوات تقديم التظلم معنا", tag="h2", size=32, align="center"),
    divider(),
])
content.append(section([steps_head], sec_settings(bg=WHITE, pad_bottom=10)))

steps = [
    ("fas fa-search", "1. دراسة قرار الرفض", "نحلّل أسباب الرفض الواردة في خطاب إدارة العلامات بدقة."),
    ("fas fa-pen-fancy", "2. إعداد مذكرة التظلم", "نصيغ تظلمًا نظاميًا مسبّبًا يدحض أسباب الرفض بالأدلة."),
    ("fas fa-paper-plane", "3. تقديم التظلم", "نرفع التظلم للجهة المختصة خلال المهلة النظامية."),
    ("fas fa-headset", "4. المتابعة حتى القبول", "نتابع الطلب ونردّ على أي ملاحظات حتى صدور القرار."),
]
s_cols = [column([icon_box(i, t, d, primary=NAVY)], 25) for (i, t, d) in steps]
content.append(section(s_cols, sec_settings(bg=WHITE, pad_top=10, pad_bottom=60)))

# --- 5. WHY US ---------------------------------------------------------------
why_head = column([
    heading("لماذا تختارنا لتقديم تظلمك؟", tag="h2", size=32, align="center", color=WHITE),
    text_editor("<p style='text-align:center;color:#D7DEEA'>نجمع بين الخبرة النظامية والمتابعة "
                "الدقيقة لرفع فرص قبول علامتك التجارية.</p>", align="center", color="#D7DEEA"),
])
content.append(section([why_head], sec_settings(gradient=True, pad_bottom=10)))

whys = [
    ("fas fa-user-tie", "خبرة متخصصة", "فريق متمرّس في تظلمات واعتراضات العلامات التجارية."),
    ("fas fa-bolt", "سرعة الاستجابة", "نلتزم بالمهل النظامية ونبدأ العمل فور تواصلك."),
    ("fas fa-shield-alt", "سرّية تامة", "نتعامل مع بياناتك ومستنداتك بخصوصية كاملة."),
    ("fas fa-hand-holding-usd", "أسعار واضحة", "تكلفة معلومة مسبقًا دون مفاجآت أو رسوم خفية."),
]
w_cols = [column([icon_box(i, t, d)], 25) for (i, t, d) in whys]
# white card look on dark bg via column background
for c in w_cols:
    c["settings"].update({
        "background_background": "classic",
        "background_color": "#13325c",
        "border_radius": {"unit": "px", "top": 12, "right": 12, "bottom": 12, "left": 12, "isLinked": True},
        "padding": {"unit": "px", "top": 26, "right": 16, "bottom": 26, "left": 16, "isLinked": False},
        "margin": {"unit": "px", "top": 0, "right": 8, "bottom": 0, "left": 8, "isLinked": False},
    })
    # text colors on dark
    for col_w in c["elements"]:
        col_w["settings"]["title_color"] = WHITE
        col_w["settings"]["description_color"] = "#C7D0DE"
content.append(section(w_cols, sec_settings(gradient=True, pad_top=10, pad_bottom=70)))

# --- 6. FAQ ------------------------------------------------------------------
faq_head = column([
    heading("الأسئلة الشائعة حول تظلم رفض العلامة التجارية", tag="h2", size=30),
    divider(),
])
faq_body = column([
    accordion([
        ("ما هي مهلة تقديم التظلم على رفض العلامة التجارية؟",
         "يجب تقديم التظلم خلال المدة النظامية المحددة في خطاب الرفض، ولذلك ننصح بالتواصل معنا فور استلام القرار لتفادي سقوط الحق."),
        ("هل يمكن قبول العلامة بعد رفضها؟",
         "نعم، كثير من قرارات الرفض يُعاد النظر فيها عند تقديم تظلم نظامي مسبّب ومدعّم بالأدلة والمستندات المناسبة."),
        ("ما المستندات المطلوبة لإعداد التظلم؟",
         "خطاب الرفض، وبيانات طلب التسجيل، وصورة العلامة، وأي مستندات تدعم أحقيتك في العلامة. ونرشدك لكل ما يلزم بعد التواصل."),
        ("هل تقدّمون صيغة تظلم من رفض تسجيل علامة تجارية جاهزة؟",
         "نُعدّ لك صيغة تظلم مخصّصة لحالتك وليست نموذجًا عامًا، لأن نجاح التظلم يعتمد على معالجة أسباب الرفض تحديدًا."),
        ("كم تستغرق إجراءات التظلم؟",
         "تختلف المدة حسب الجهة وطبيعة الحالة، ونحرص على تقديم التظلم مبكرًا ومتابعته حتى صدور القرار النهائي."),
    ]),
])
content.append(section([faq_head, faq_body], sec_settings(bg=WHITE, pad_top=60, pad_bottom=60)))

# --- 7. FINAL CTA ------------------------------------------------------------
cta_col = column([
    heading("ابدأ تظلمك الآن قبل انتهاء المهلة النظامية", tag="h2", size=32, align="center", color=NAVY),
    text_editor("<p style='text-align:center'>تواصل معنا اليوم للحصول على استشارة حول تظلم رفض "
                "علامتك التجارية والبدء في إعداد مذكرتك.</p>", align="center", color=NAVY),
    spacer(10),
    inner_section([
        column([button("📞 اتصل: %s" % PHONE_DISPLAY, TEL_LINK, bg=NAVY, color=WHITE, align="center", icon="fas fa-phone-alt")], 50),
        column([button("واتساب مباشر", WA_LINK, bg="#25D366", color=WHITE, align="center", icon="fab fa-whatsapp")], 50),
    ], {"gap": "default"}),
])
content.append(section([cta_col], sec_settings(bg=GOLD, pad_top=70, pad_bottom=70)))

# --- 8. FOOTER ---------------------------------------------------------------
footer_col = column([
    heading("خدمة %s" % SERVICE_NAME, tag="h3", size=20, align="center", color=WHITE),
    text_editor(
        "<p style='text-align:center;color:#C7D0DE'>نقدّم خدمات التظلم والاعتراض على قرارات "
        "العلامات التجارية في المملكة العربية السعودية.</p>"
        "<p style='text-align:center;color:#FFFFFF'>للتواصل: %s</p>" % PHONE_DISPLAY,
        align="center", color="#C7D0DE"),
    text_editor("<p style='text-align:center;color:#7E8aa0;font-size:13px'>"
                "جميع الحقوق محفوظة © 2026</p>", align="center", color="#7E8aa0"),
])
content.append(section([footer_col], sec_settings(bg=NAVY, pad_top=40, pad_bottom=40)))

# ===========================================================================
# Page settings + envelope
# ===========================================================================
page_settings = {
    "template": "elementor_canvas",
    "hide_title": "yes",
    "page_title": SERVICE_NAME,
}

template = {
    "version": "0.4",
    "title": "تظلم رفض العلامة التجارية - صفحة هبوط",
    "type": "page",
    "page_settings": page_settings,
    "content": content,
}

out_path = os.path.join(os.path.dirname(__file__), "elementor-template.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print("Wrote %s (%d top-level sections)" % (out_path, len(content)))
