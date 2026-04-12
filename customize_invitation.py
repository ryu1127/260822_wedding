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
    "groom": {
        "name": "류동헌", "phone": "010-2923-7726",
        "father": "류부열", "mother": "김태옥"
    },
    "bride": {
        "name": "황혜신", "phone": "010-6334-6843",
        "father": "황애민", "mother": "안미옥"
    },
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
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang&display=swap');
        
        :root {
            --bg-color: #fefcf3;
            --text-color: #000000;
            --accent-color: #bd7d1e;
            --gray-text: #666666;
            --white: #ffffff;
        }

        body { font-family: 'Gowun Batang', serif; margin: 0; padding: 0; background-color: var(--bg-color); color: var(--text-color); display: flex; justify-content: center; }
        .container { max-width: 480px; width: 100%; background: var(--white); box-shadow: 0 0 20px rgba(0,0,0,0.05); overflow-x: hidden; position: relative; }
        
        .section { padding: 60px 20px; text-align: center; border-bottom: 1px solid #f0f0f0; }
        
        .reveal { opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; }
        .reveal.active { opacity: 1; transform: translateY(0); }

        .main-photo-wrap { position: relative; width: 100%; }
        .main-photo img { width: 100%; display: block; }
        .d-day-badge { 
            position: absolute; top: 20px; right: 20px; 
            background: rgba(189, 125, 30, 0.85); color: #fff; 
            padding: 8px 15px; border-radius: 20px; font-size: 14px; 
            letter-spacing: 1px; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            z-index: 10;
        }

        .names { font-size: 24px; margin-bottom: 10px; color: var(--accent-color); font-weight: bold; }
        .names span { font-size: 18px; vertical-align: middle; margin: 0 5px; opacity: 0.8; }
        .date-info { font-size: 16px; color: var(--gray-text); margin-bottom: 30px; }

        .family-section { display: flex; justify-content: space-around; align-items: flex-start; margin: 30px 0; border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 30px 0; }
        .family-side { flex: 1; text-align: center; }
        .family-side:first-child { border-right: 1px solid #eee; }
        .family-parents { font-size: 16px; margin-bottom: 8px; line-height: 1.6; display: flex; justify-content: center; gap: 5px; }
        .family-parents span.amp { font-size: 14px; color: #aaa; margin: 0 2px; }
        .family-relation { font-size: 13px; color: #888; margin-bottom: 5px; }
        .family-child { font-size: 18px; font-weight: bold; color: var(--accent-color); }

        .swiper-gallery { width: 100%; height: 480px; margin: 20px 0; }
        .swiper-slide-gallery { display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr); gap: 10px; padding: 10px; box-sizing: border-box; }
        .swiper-slide-gallery img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; cursor: pointer; aspect-ratio: 1/1; }
        
        #lightbox { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95); z-index: 2000; flex-direction: column; justify-content: center; align-items: center; }
        .swiper-lightbox { width: 100%; height: 100%; }
        .swiper-slide-lightbox { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }
        .swiper-slide-lightbox img { max-width: 100%; max-height: 90vh; object-fit: contain; }
        #lightbox .close { position: absolute; top: 30px; right: 20px; color: #fff; font-size: 40px; cursor: pointer; z-index: 2100; padding: 10px; line-height: 1; }

        .box-style { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 20px; text-align: left; border: 1px solid #eee; }
        .account-item { margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        .account-item:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
        .account-info { display: flex; justify-content: space-between; align-items: center; margin-top: 5px; }
        
        .btn-group { display: flex; gap: 5px; }
        .small-btn { padding: 6px 12px; background: var(--accent-color); color: #fff; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; text-decoration: none; display: inline-block; }
        .phone-btn { background: #8e9775; display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; padding: 0; } 
        
        .share-btn { background: var(--accent-color); color: #fff; font-weight: bold; width: 100%; margin-top: 10px; height: 45px; font-size: 14px; border-radius: 8px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .flower-btn { background: var(--white); color: #333; border: 1px solid #ddd; width: 100%; margin-top: 10px; height: 45px; font-size: 14px; border-radius: 8px; cursor: pointer; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 8px; }

        .map-container { width: 100%; height: 350px; margin: 20px 0; border-radius: 8px; overflow: hidden; border: 1px solid #eee; }
        .map-btn-group { display: flex; gap: 8px; justify-content: center; margin-top: 10px; flex-wrap: wrap; }
        .map-btn { padding: 10px 12px; background: var(--accent-color); color: #fff; text-decoration: none; border-radius: 20px; font-size: 12px; min-width: 80px; text-align: center; }
        .kakao-btn { background: #fee500; color: #3c1e1e; }
        .tmap-btn { background: #1a73e8; color: #fff; }
        
        .transport-item { text-align: left; margin-bottom: 25px; padding-left: 10px; border-left: 2px solid var(--accent-color); }
        .transport-title { font-weight: bold; color: var(--accent-color); font-size: 15px; margin-bottom: 5px; }
        .transport-desc { font-size: 14px; color: #666; line-height: 1.6; }
        .footer { padding: 40px; text-align: center; font-size: 12px; color: #aaa; background: #fafafa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-photo-wrap">
            <div class="d-day-badge" id="d-day-text">D-Day</div>
            <div class="main-photo"><img src="{{cover_photo}}" alt="Cover"></div>
        </div>
        
        <div class="section reveal">
            <div class="names">{{groom_name}} <span>♥</span> {{bride_name}}</div>
            <div class="date-info">2026. 08. 22 토요일 12:30</div>
            
            <div class="family-section">
                <div class="family-side">
                    <div class="family-parents">
                        {{groom_father}}<span class="amp">&</span>{{groom_mother}}
                    </div>
                    <div class="family-relation">아들</div>
                    <div class="family-child">{{groom_name}}</div>
                </div>
                <div class="family-side">
                    <div class="family-parents">
                        {{bride_father}}<span class="amp">&</span>{{bride_mother}}
                    </div>
                    <div class="family-relation">딸</div>
                    <div class="family-child">{{bride_name}}</div>
                </div>
            </div>
            
            <div style="margin-top: 20px; font-size: 15px;">노블발렌티 <span style="font-weight:bold;">대치점</span> {{hall_detail}}</div>
        </div>

        <div class="section greeting reveal">
            <h2 style="color: var(--accent-color); font-weight: normal; letter-spacing: 2px;">{{greeting_title}}</h2>
            <p style="line-height: 2.2; white-space: pre-wrap; font-size: 15px;">{{greeting_message}}</p>
        </div>

        <div class="section reveal" style="padding: 60px 0;">
            <h2 style="color: var(--accent-color); font-weight: normal; letter-spacing: 2px;">Wedding Gallery</h2>
            <div class="swiper swiper-gallery">
                <div class="swiper-wrapper" id="gallery-wrapper"></div>
                <div class="swiper-button-next" style="color: var(--accent-color);"></div>
                <div class="swiper-button-prev" style="color: var(--accent-color);"></div>
            </div>
        </div>

        <div class="section venue reveal">
            <h2 style="color: var(--accent-color); font-weight: normal; letter-spacing: 2px;">오시는 길</h2>
            <p style="margin-bottom: 5px;"><strong>노블발렌티 <span style="font-weight:bold;">대치점</span> {{hall_detail}}</strong></p>
            <p class="note-subtitle">*삼성점이 아니오니 유의 부탁드립니다.</p>
            <p style="font-size: 14px; color: #444;">{{address}}</p>
            
            <div class="map-container">
                <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3165.140461243454!2d127.0632663763564!3d37.50330422701411!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x357ca44090900001%3A0x2f8f0f0f0f0f0f0f!2z64W467iU67Cc66CM7YisIOuMgOueygkA!5e0!3m2!1sko!2skr!4v1712920000000!5m2!1sko!2skr" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
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

        <div class="section reveal">
            <h2 style="color: var(--accent-color); font-weight: normal; letter-spacing: 2px;">마음 전하실 곳</h2>
            <div class="box-style">{{account_items_html}}</div>
            
            <div style="margin-top: 20px;">
                <a href="https://m.99flower.co.kr/" target="_blank" class="flower-btn">🌸 축하 화환 보내기</a>
                <button class="share-btn" onclick="shareInvitation()">🔗 모바일 청첩장 링크 공유하기</button>
            </div>
        </div>

        <div class="footer">© {{wedding_year}} {{groom_name}} & {{bride_name}}</div>
    </div>

    <div id="lightbox">
        <span class="close" onclick="closeLightbox()">&times;</span>
        <div class="swiper swiper-lightbox">
            <div class="swiper-wrapper" id="lightbox-wrapper"></div>
            <div class="swiper-button-next"></div>
            <div class="swiper-button-prev"></div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
    <script>
        const weddingDate = new Date("2026-08-22").getTime();
        const now = new Date().getTime();
        const dDayCount = Math.ceil((weddingDate - now) / (1000 * 60 * 60 * 24));
        const dDayElement = document.getElementById('d-day-text');
        if (dDayCount > 0) dDayElement.innerText = `D-${dDayCount}`;
        else if (dDayCount === 0) dDayElement.innerText = `D-Day`;
        else dDayElement.style.display = 'none';

        const reveals = document.querySelectorAll('.reveal');
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) entry.target.classList.add('active');
                else entry.target.classList.remove('active');
            });
        }, { threshold: 0.1 });
        reveals.forEach(r => observer.observe(r));

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
        const lightboxSwiper = new Swiper('.swiper-lightbox', { slidesPerView: 1, spaceBetween: 0, loop: true, observer: true, observeParents: true, navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }, preventClicks: false, preventClicksPropagation: false, touchStartPreventDefault: false });

        function openLightbox(idx) { document.getElementById('lightbox').style.display = 'flex'; lightboxSwiper.update(); setTimeout(() => { lightboxSwiper.slideToLoop(idx, 0); }, 50); document.body.style.overflow = 'hidden'; }
        function closeLightbox() { document.getElementById('lightbox').style.display = 'none'; document.body.style.overflow = 'auto'; }
        function copyToClipboard(text) { navigator.clipboard.writeText(text).then(() => alert('계좌번호가 복사되었습니다.')); }

        function shareInvitation() {
            if (navigator.share) {
                navigator.share({ title: '{{groom_name}} ♥ {{bride_name}} 결혼합니다', text: '저희 두사람의 결혼식에 소중한 분들을 초대합니다.', url: window.location.href }).catch(console.error);
            } else {
                navigator.clipboard.writeText(window.location.href).then(() => { alert('청첩장 링크가 복사되었습니다.'); });
            }
        }
    </script>
</body>
</html>
"""
    account_html = ""
    for acc in data['accounts']:
        account_html += f"""<div class="account-item"><strong>{acc['owner']}</strong><div class="account-info"><small style="color:#666;">{acc['bank']} {acc['number']}</small><div class="btn-group"><a href="tel:{acc['phone']}" class="small-btn phone-btn">📞</a><button class="small-btn" onclick="copyToClipboard('{acc['number'].replace("-", "")}')">복사</button></div></div></div>"""

    html_content = template_text
    html_content = html_content.replace("{{groom_name}}", data['groom']['name']).replace("{{bride_name}}", data['bride']['name'])
    html_content = html_content.replace("{{groom_father}}", data['groom']['father']).replace("{{groom_mother}}", data['groom']['mother'])
    html_content = html_content.replace("{{bride_father}}", data['bride']['father']).replace("{{bride_mother}}", data['bride']['mother'])
    html_content = html_content.replace("{{hall_detail}}", data['hall_detail']).replace("{{address}}", data['address'])
    html_content = html_content.replace("{{greeting_title}}", data['greeting_title']).replace("{{greeting_message}}", data['greeting_message'])
    html_content = html_content.replace("{{cover_photo}}", cover_photo)
    html_content = html_content.replace("{{subway}}", data['transportation']['subway']).replace("{{bus}}", data['transportation']['bus']).replace("{{parking}}", data['transportation']['parking'])
    html_content = html_content.replace("{{wedding_year}}", data['wedding_date'].split('-')[0]).replace("{{account_items_html}}", account_html)
    html_content = html_content.replace("{{photo_data_json}}", json.dumps(data['photos']))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Refined invitation with updated symbols generated at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_invitation_html(MY_DATA)
    os.system(f"open index.html")
