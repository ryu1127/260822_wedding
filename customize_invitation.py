import json
import os
import glob
import shutil
from PIL import Image

# 1. Configuration
SOURCE_PHOTO_FOLDER = "/Users/dongheonryu/Downloads/0302/최종보정본"
IMAGES_DIR = "images"
THUMBNAILS_DIR = "thumbnails"

for d in [IMAGES_DIR, THUMBNAILS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

all_source_photos = sorted(glob.glob(os.path.join(SOURCE_PHOTO_FOLDER, "*.jpg")))

photo_data = []
print("Preparing optimized photos...")

MAX_FULL_SIZE = (1200, 1200) 
THUMB_SIZE = (400, 400)

for p in all_source_photos:
    filename = os.path.basename(p)
    dest_image_path = os.path.join(IMAGES_DIR, filename)
    thumb_path = os.path.join(THUMBNAILS_DIR, filename)
    
    if not os.path.exists(dest_image_path):
        with Image.open(p) as img:
            img.thumbnail(MAX_FULL_SIZE)
            img.save(dest_image_path, "JPEG", quality=75, optimize=True)
        
    if not os.path.exists(thumb_path):
        with Image.open(p) as img:
            img.thumbnail(THUMB_SIZE)
            img.save(thumb_path, "JPEG", quality=75)
            
    photo_data.append({
        "full": f"images/{filename}",
        "thumb": f"thumbnails/{filename}"
    })

MY_DATA = {
    "groom_name": "류동헌", "groom_phone": "010-2923-7726",
    "bride_name": "황혜신", "bride_phone": "010-6334-6843",
    "wedding_date": "2026-08-22", "wedding_time": "12:30",
    "venue_name": "노블발렌티 대치점", "hall_detail": "B1 단독홀",
    "address": "서울특별시 강남구 영동대로 325 (S-Tower 지하 1층)",
    "greeting_title": "우리, 결혼합니다",
    "greeting_message": "저희 두사람의 작은 만남이\n사랑의 결실을 이루어\n결혼식을 올리게 되었습니다.\n\n평생 서로를 귀하게 여기며 첫 마음\n그대로 존중하고 배려하며 살겠습니다.",
    "photos": photo_data,
    "transportation": {
        "subway": "2호선 삼성역 3번 출구 (셔틀버스 수시 운행)<br>3호선 학여울역 1번 출구 (도보 10분)",
        "bus": "휘문고교 사거리 정류장 하차<br>간선: 343, 401 / 지선: 4319 / 마을: 강남01, 강남06",
        "parking": "S-Tower 건물 내 지하 주차장 (하객 2시간 무료)"
    },
    "accounts": [
        {"owner": "신랑 류동헌", "bank": "토스뱅크", "number": "1000-1013-9845", "phone": "010-2923-7726"},
        {"owner": "신부 황혜신", "bank": "토스뱅크", "number": "1000-2458-9041", "phone": "010-6334-6843"}
    ]
}

def generate_invitation_html(data, output_path="index.html"):
    cover_photo = data['photos'][0]['full'] if data['photos'] else ""
    
    template_text = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{groom_name}} ♥ {{bride_name}} 결혼합니다</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
    <!-- Kakao SDK -->
    <script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.0/kakao.min.js" integrity="sha384-l6S9p9NoAn7GnEALcaS7Ssh9vYpYpHshGRGwZf9f9ksNCfIzZ6XnxnVvIn2OnYka" crossorigin="anonymous"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');
        body { font-family: 'Gowun Batang', serif; margin: 0; padding: 0; background-color: #fefcf3; color: #333; display: flex; justify-content: center; }
        .container { max-width: 480px; width: 100%; background: #fff; box-shadow: 0 0 20px rgba(0,0,0,0.05); overflow-x: hidden; position: relative; }
        .section { padding: 60px 20px; text-align: center; border-bottom: 1px solid #f0f0f0; }
        
        /* D-Day Top Bar */
        .d-day-top { background: #bd7d1e; color: #fff; padding: 10px; font-size: 14px; letter-spacing: 2px; position: sticky; top: 0; z-index: 100; }

        .main-photo img { width: 100%; display: block; }
        .names { font-size: 24px; margin-bottom: 10px; color: #bd7d1e; }
        .date-info { font-size: 16px; color: #888; margin-bottom: 30px; }
        .note-subtitle { font-size: 13px; color: #999; margin-top: -10px; margin-bottom: 20px; }

        .swiper-gallery { width: 100%; height: 480px; margin: 20px 0; }
        .swiper-slide-gallery { display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr); gap: 10px; padding: 10px; box-sizing: border-box; }
        .swiper-slide-gallery img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; cursor: pointer; aspect-ratio: 1/1; }
        
        #lightbox { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95); z-index: 2000; flex-direction: column; justify-content: center; align-items: center; }
        .swiper-lightbox { width: 100%; height: 100%; }
        .swiper-slide-lightbox { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }
        .swiper-slide-lightbox img { max-width: 100%; max-height: 90vh; object-fit: contain; display: block; }
        #lightbox .close { position: absolute; top: 30px; right: 20px; color: #fff; font-size: 40px; cursor: pointer; z-index: 2100; padding: 10px; line-height: 1; }

        .box-style { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 20px; text-align: left; border: 1px solid #eee; }
        .account-item { margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .account-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        .account-info { display: flex; justify-content: space-between; align-items: center; margin-top: 5px; }
        .btn-group { display: flex; gap: 5px; }
        .small-btn { padding: 6px 12px; background: #bd7d1e; color: #fff; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; text-decoration: none; display: inline-block; }
        .phone-btn { background: #5cb85c; }
        .share-btn { background: #fee500; color: #3c1e1e; font-weight: bold; width: 100%; margin-top: 10px; height: 45px; font-size: 14px; border-radius: 8px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .flower-btn { background: #fff; color: #333; border: 1px solid #ddd; width: 100%; margin-top: 10px; height: 45px; font-size: 14px; border-radius: 8px; cursor: pointer; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; }

        /* Naver Map Style Container */
        .map-preview { 
            width: 100%; height: 220px; background: #f0f0f0; border-radius: 8px; margin: 20px 0; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            border: 1px solid #ddd; background-image: url('https://upload.wikimedia.org/wikipedia/commons/b/bc/Naver_Map_Logo.png');
            background-size: 60px; background-repeat: no-repeat; background-position: center 60px;
            position: relative; cursor: pointer;
        }
        .map-preview::after { content: "네이버 지도로 바로가기"; position: absolute; bottom: 60px; font-weight: bold; color: #03c75a; }
        .map-preview-btn { position: absolute; bottom: 20px; background: #03c75a; color: #fff; padding: 8px 20px; border-radius: 4px; font-size: 13px; font-weight: bold; }

        .map-btn-group { display: flex; gap: 8px; justify-content: center; margin-top: 10px; flex-wrap: wrap; }
        .map-btn { padding: 10px 12px; background: #bd7d1e; color: #fff; text-decoration: none; border-radius: 20px; font-size: 12px; min-width: 80px; text-align: center; }
        .kakao-btn { background: #fee500; color: #3c1e1e; }
        .tmap-btn { background: #1a73e8; color: #fff; }
        
        .transport-item { text-align: left; margin-bottom: 25px; padding-left: 10px; border-left: 2px solid #f3d090; }
        .transport-title { font-weight: bold; color: #bd7d1e; font-size: 15px; margin-bottom: 5px; }
        .transport-desc { font-size: 14px; color: #666; line-height: 1.6; }
        .footer { padding: 40px; text-align: center; font-size: 12px; color: #aaa; background: #fafafa; }
    </style>
</head>
<body>
    <div class="d-day-top" id="d-day-display">LOADING...</div>
    <div class="container">
        <div class="main-photo"><img src="{{cover_photo}}" alt="Cover"></div>
        <div class="section">
            <div class="names">{{groom_name}} & {{bride_name}}</div>
            <div class="date-info">2026. 08. 22 토요일 12:30</div>
            <div>노블발렌티 <span style="font-weight:bold;">대치점</span> {{hall_detail}}</div>
        </div>

        <div class="section greeting">
            <h2 style="color: #bd7d1e;">{{greeting_title}}</h2>
            <p style="line-height: 2; white-space: pre-wrap;">{{greeting_message}}</p>
        </div>

        <div class="section" style="padding: 60px 0;">
            <h2 style="color: #bd7d1e;">Wedding Gallery</h2>
            <div class="swiper swiper-gallery">
                <div class="swiper-wrapper" id="gallery-wrapper"></div>
                <div class="swiper-button-next" style="color: #bd7d1e;"></div>
                <div class="swiper-button-prev" style="color: #bd7d1e;"></div>
            </div>
        </div>

        <div class="section venue">
            <h2 style="color: #bd7d1e;">오시는 길</h2>
            <p style="margin-bottom: 5px;"><strong>노블발렌티 <span style="font-weight:bold;">대치점</span> {{hall_detail}}</strong></p>
            <p class="note-subtitle">*삼성점이 아니오니 유의 부탁드립니다.</p>
            <p style="font-size: 14px; color: #888;">{{address}}</p>
            
            <!-- Naver Map Placeholder Link -->
            <div class="map-preview" onclick="window.open('https://map.naver.com/v5/search/%EB%85%B8%EB%B8%94%EB%B0%9C%EB%A0%8C%ED%8B%B0%20%EB%8C%80%EC%B9%98', '_blank')">
                <div class="map-preview-btn">네이버 지도 앱 열기</div>
            </div>

            <div class="map-btn-group">
                <a href="https://surl.tmap.co.kr/6866666c" target="_blank" class="map-btn tmap-btn">티맵</a>
                <a href="https://map.naver.com/v5/search/%EB%85%B8%EB%B8%94%EB%B0%9C%EB%A0%8C%ED%8B%B0%20%EB%8C%80%EC%B9%98" target="_blank" class="map-btn">네이버 지도</a>
                <a href="https://map.kakao.com/link/search/%EB%85%B8%EB%B8%94%EB%B0%9C%EB%A0%8C%ED%8B%B0%20%EB%8C%80%EC%B9%98%EC%A0%90" target="_blank" class="map-btn kakao-btn">카카오 맵</a>
            </div>
            <div style="margin-top: 40px;">
                <div class="transport-item"><div class="transport-title">지하철 및 셔틀버스</div><div class="transport-desc">{{subway}}</div></div>
                <div class="transport-item"><div class="transport-title">버스</div><div class="transport-desc">{{bus}}</div></div>
                <div class="transport-item"><div class="transport-title">주차 안내</div><div class="transport-desc">{{parking}}</div></div>
            </div>
        </div>

        <div class="section">
            <h2 style="color: #bd7d1e;">마음 전하실 곳</h2>
            <div class="box-style">{{account_items_html}}</div>
            
            <a href="https://m.99flower.co.kr/" target="_blank" class="flower-btn">
                🌸 축하 화환 보내기
            </a>
            
            <button class="share-btn" onclick="shareKakao()">
                💬 카카오톡으로 청첩장 공유하기
            </button>
        </div>

        <div class="footer">© {{wedding_year}} {{groom_name}} & {{bride_name}}</div>
    </div>

    <div id="lightbox">
        <span class="close" onclick="closeLightbox()">&times;</span>
        <div class="swiper swiper-lightbox">
            <div class="swiper-wrapper" id="lightbox-wrapper"></div>
            <div class="swiper-button-next" style="color: #fff;"></div>
            <div class="swiper-button-prev" style="color: #fff;"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        // 1. D-Day Logic
        const weddingDate = new Date("2026-08-22").getTime();
        function updateDDay() {
            const now = new Date().getTime();
            const distance = weddingDate - now;
            const days = Math.ceil(distance / (1000 * 60 * 60 * 24));
            const display = document.getElementById('d-day-display');
            if (days > 0) display.innerText = `2026. 08. 22 (D-${days})`;
            else if (days === 0) display.innerText = `HAPPY WEDDING DAY (D-Day)`;
            else display.innerText = `2026. 08. 22`;
        }
        updateDDay();

        // 2. Photo Data
        const photoData = {{photo_data_json}};
        const galleryWrapper = document.getElementById('gallery-wrapper');
        const lightboxWrapper = document.getElementById('lightbox-wrapper');
        
        for (let i = 0; i < photoData.length; i += 4) {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide swiper-slide-gallery';
            photoData.slice(i, i + 4).forEach((photo, idx) => {
                const img = document.createElement('img');
                img.src = photo.thumb;
                img.onclick = () => openLightbox(i + idx);
                slide.appendChild(img);
            });
            galleryWrapper.appendChild(slide);
        }

        photoData.forEach(photo => {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide swiper-slide-lightbox';
            const img = document.createElement('img');
            img.src = photo.full;
            img.loading = 'lazy';
            slide.appendChild(img);
            lightboxWrapper.appendChild(slide);
        });

        const gallerySwiper = new Swiper('.swiper-gallery', { slidesPerView: 1, spaceBetween: 10, navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' } });
        const lightboxSwiper = new Swiper('.swiper-lightbox', { slidesPerView: 1, spaceBetween: 0, loop: true, navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' } });

        function openLightbox(idx) { document.getElementById('lightbox').style.display = 'flex'; lightboxSwiper.update(); lightboxSwiper.slideToLoop(idx, 0); document.body.style.overflow = 'hidden'; }
        function closeLightbox() { document.getElementById('lightbox').style.display = 'none'; document.body.style.overflow = 'auto'; }
        
        // 3. Utils
        function copyToClipboard(text) { navigator.clipboard.writeText(text).then(() => alert('계좌번호가 복사되었습니다.')); }

        // 4. Kakao Share
        Kakao.init('7e2f0606066060606060606060606060'); // API Key placeholder - JavaScript Key needed for full functionality
        function shareKakao() {
            if (!Kakao.isInitialized()) {
                alert('카카오톡 공유 기능을 준비 중입니다. 링크를 직접 복사해 주세요.');
                return;
            }
            Kakao.Share.sendDefault({
                objectType: 'feed',
                content: {
                    title: '류동헌 ♥ 황혜신 결혼합니다',
                    description: '2026. 08. 22 12:30 노블발렌티 대치점',
                    imageUrl: window.location.origin + '/{{cover_photo}}',
                    link: { mobileWebUrl: window.location.href, webUrl: window.location.href },
                },
                buttons: [{ title: '청첩장 보기', link: { mobileWebUrl: window.location.href, webUrl: window.location.href } }]
            });
        }
    </script>
</body>
</html>
"""
    # Generate Account & Phone HTML
    account_html = ""
    for acc in data['accounts']:
        account_html += f"""
        <div class="account-item">
            <strong>{acc['owner']}</strong>
            <div class="account-info">
                <small style="color:#666;">{acc['bank']} {acc['number']}</small>
                <div class="btn-group">
                    <a href="tel:{acc['phone']}" class="small-btn phone-btn">전화</a>
                    <button class="small-btn" onclick="copyToClipboard('{acc['number'].replace("-", "")}')">복사</button>
                </div>
            </div>
        </div>"""

    # Manual replacement
    html_content = template_text
    html_content = html_content.replace("{{groom_name}}", data['groom_name']).replace("{{bride_name}}", data['bride_name'])
    html_content = html_content.replace("{{wedding_date}}", data['wedding_date'])
    html_content = html_content.replace("{{hall_detail}}", data['hall_detail']).replace("{{address}}", data['address'])
    html_content = html_content.replace("{{greeting_title}}", data['greeting_title']).replace("{{greeting_message}}", data['greeting_message'])
    html_content = html_content.replace("{{cover_photo}}", cover_photo)
    html_content = html_content.replace("{{subway}}", data['transportation']['subway']).replace("{{bus}}", data['transportation']['bus']).replace("{{parking}}", data['transportation']['parking'])
    html_content = html_content.replace("{{wedding_year}}", data['wedding_date'].split('-')[0]).replace("{{account_items_html}}", account_html)
    html_content = html_content.replace("{{photo_data_json}}", json.dumps(data['photos']))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Final feature-rich invitation generated at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_invitation_html(MY_DATA)
    os.system(f"open index.html")
