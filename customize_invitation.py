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
print("Re-optimizing photos for better mobile compatibility...")

# 모바일 환경을 고려하여 해상도를 조금 더 줄임 (1200px이면 폰에서는 충분히 고화질입니다)
MAX_FULL_SIZE = (1200, 1200) 
THUMB_SIZE = (400, 400)

for p in all_source_photos:
    filename = os.path.basename(p)
    dest_image_path = os.path.join(IMAGES_DIR, filename)
    thumb_path = os.path.join(THUMBNAILS_DIR, filename)
    
    # 무조건 다시 최적화하여 덮어쓰기 (용량과 해상도 확실히 줄임)
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
    "groom_name": "류동헌", "bride_name": "황혜신",
    "wedding_date": "2026-08-22", "wedding_time": "12:30",
    "venue_name": "노블발렌티 대치점", "hall_detail": "B1 단독홀",
    "address": "서울특별시 강남구 영동대로 325 (S-Tower 지하 1층)",
    "greeting_title": "우리, 결혼합니다",
    "greeting_message": "저희 두사람의 작은 만남이\n사랑의 결실을 이루어\n결혼식을 올리게 되었습니다.\n\n평생 서로를 귀하게 여기며 첫 마음\n그대로 존중하고 배려하며 살겠습니다.",
    "photos": photo_data,
    "map_image_url": "https://cdn.imweb.me/thumbnail/20251224/804939816d76a.jpg",
    "transportation": {
        "subway": "2호선 삼성역 3번 출구 (셔틀버스 수시 운행)<br>3호선 학여울역 1번 출구 (도보 10분)",
        "bus": "휘문고교 사거리 정류장 하차<br>간선: 343, 401 / 지선: 4319 / 마을: 강남01, 강남06",
        "parking": "S-Tower 건물 내 지하 주차장 (하객 2시간 무료)"
    },
    "accounts": [
        {"owner": "신랑 류동헌", "bank": "토스뱅크", "number": "1000-1013-9845"},
        {"owner": "신부 황혜신", "bank": "토스뱅크", "number": "1000-2458-9041"}
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
        body { font-family: 'Gowun Batang', serif; margin: 0; padding: 0; background-color: #fefcf3; color: #333; display: flex; justify-content: center; }
        .container { max-width: 480px; width: 100%; background: #fff; box-shadow: 0 0 20px rgba(0,0,0,0.05); overflow-x: hidden; }
        .section { padding: 60px 20px; text-align: center; border-bottom: 1px solid #f0f0f0; }
        .main-photo img { width: 100%; display: block; }
        .names { font-size: 24px; margin-bottom: 10px; color: #bd7d1e; }
        .date-info { font-size: 16px; color: #888; margin-bottom: 30px; }
        .note-subtitle { font-size: 13px; color: #999; margin-top: -10px; margin-bottom: 20px; }

        /* Gallery */
        .swiper-gallery { width: 100%; height: 480px; margin: 20px 0; }
        .swiper-slide-gallery { display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: repeat(2, 1fr); gap: 10px; padding: 10px; box-sizing: border-box; }
        .swiper-slide-gallery img { width: 100%; height: 100%; object-fit: cover; border-radius: 4px; cursor: pointer; aspect-ratio: 1/1; }
        
        /* Lightbox - Fixed display issue */
        #lightbox { display: none; position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.95); z-index: 2000; flex-direction: column; justify-content: center; align-items: center; }
        .swiper-lightbox { width: 100%; height: 100%; }
        .swiper-slide-lightbox { display: flex; justify-content: center; align-items: center; width: 100%; height: 100%; }
        .swiper-slide-lightbox img { max-width: 100%; max-height: 90vh; object-fit: contain; display: block; }
        #lightbox .close { position: absolute; top: 30px; right: 20px; color: #fff; font-size: 40px; cursor: pointer; z-index: 2100; padding: 10px; line-height: 1; }

        .box-style { background: #f9f9f9; padding: 20px; border-radius: 8px; margin-top: 20px; text-align: left; border: 1px solid #eee; }
        .account-item { margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
        .copy-btn { padding: 5px 10px; background: #bd7d1e; color: #fff; border: none; border-radius: 4px; font-size: 12px; cursor: pointer; }

        .guestbook-input { width: 100%; margin-bottom: 10px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-family: inherit; }
        .guestbook-list { margin-top: 20px; text-align: left; }
        .guestbook-item { padding: 12px; border-bottom: 1px solid #f0f0f0; background: #fff; margin-bottom: 8px; border-radius: 4px; }
        .guestbook-name { font-weight: bold; font-size: 14px; color: #bd7d1e; margin-bottom: 4px; }
        .guestbook-msg { font-size: 14px; color: #444; line-height: 1.4; }

        .pagination { display: flex; justify-content: center; align-items: center; gap: 15px; margin-top: 20px; }
        .page-btn { padding: 5px 12px; border: 1px solid #bd7d1e; background: #fff; color: #bd7d1e; border-radius: 4px; cursor: pointer; font-size: 13px; }
        .page-btn:disabled { border-color: #ddd; color: #ccc; cursor: default; }

        .map-wrapper { margin: 20px 0; border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
        .map-wrapper img { width: 100%; display: block; }
        .map-btn-group { display: flex; gap: 10px; justify-content: center; margin-top: 10px; }
        .map-btn { padding: 10px 15px; background: #bd7d1e; color: #fff; text-decoration: none; border-radius: 20px; font-size: 13px; }
        .kakao-btn { background: #fee500; color: #3c1e1e; }
        
        .transport-item { text-align: left; margin-bottom: 25px; padding-left: 10px; border-left: 2px solid #f3d090; }
        .transport-title { font-weight: bold; color: #bd7d1e; font-size: 15px; margin-bottom: 5px; }
        .transport-desc { font-size: 14px; color: #666; line-height: 1.6; }
        .footer { padding: 40px; text-align: center; font-size: 12px; color: #aaa; background: #fafafa; }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-photo"><img src="{{cover_photo}}" alt="Cover"></div>
        <div class="section">
            <div class="names">{{groom_name}} & {{bride_name}}</div>
            <div class="date-info">{{wedding_date}} {{wedding_time}}</div>
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
            <div class="map-wrapper"><img src="{{map_image_url}}" alt="Map"></div>
            <div class="map-btn-group">
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
        </div>

        <div class="section">
            <h2 style="color: #bd7d1e;">방명록</h2>
            <div class="box-style">
                <input type="text" id="gb-name" class="guestbook-input" placeholder="성함을 입력해주세요">
                <textarea id="gb-msg" class="guestbook-input" placeholder="축하 메시지를 남겨주세요" rows="3"></textarea>
                <button class="copy-btn" style="width: 100%; height: 40px; font-size: 14px;" onclick="addGuestbook()">메시지 남기기</button>
                <div id="gb-list" class="guestbook-list"></div>
                <div class="pagination" id="pagination"></div>
            </div>
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
            img.src = photo.full; // Use standard src for reliability
            img.loading = 'lazy';
            slide.appendChild(img);
            lightboxWrapper.appendChild(slide);
        });

        const gallerySwiper = new Swiper('.swiper-gallery', { 
            slidesPerView: 1, 
            spaceBetween: 10, 
            navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' } 
        });
        
        const lightboxSwiper = new Swiper('.swiper-lightbox', { 
            slidesPerView: 1, 
            spaceBetween: 0, 
            loop: true,
            navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' } 
        });

        function openLightbox(idx) { 
            document.getElementById('lightbox').style.display = 'flex'; 
            lightboxSwiper.update(); // Refresh swiper calculation
            lightboxSwiper.slideToLoop(idx, 0); 
            document.body.style.overflow = 'hidden'; 
        }
        function closeLightbox() { 
            document.getElementById('lightbox').style.display = 'none'; 
            document.body.style.overflow = 'auto'; 
        }
        function copyToClipboard(text) { navigator.clipboard.writeText(text).then(() => alert('계좌번호가 복사되었습니다.')); }

        let currentPage = 1; const pageSize = 5;
        function loadGuestbook() {
            const fullList = JSON.parse(localStorage.getItem('wedding_gb') || '[]').reverse();
            const totalItems = fullList.length; const totalPages = Math.ceil(totalItems / pageSize);
            if (currentPage > totalPages && totalPages > 0) currentPage = totalPages;
            const startIndex = (currentPage - 1) * pageSize;
            const pagedList = fullList.slice(startIndex, startIndex + pageSize);
            const container = document.getElementById('gb-list');
            if (pagedList.length === 0) {
                container.innerHTML = '<p style="text-align:center; color:#999; font-size:13px; margin:20px 0;">첫 번째 축하 메시지를 남겨주세요.</p>';
                document.getElementById('pagination').innerHTML = ''; return;
            }
            container.innerHTML = pagedList.map(item => `<div class="guestbook-item"><div class="guestbook-name">${item.name}</div><div class="guestbook-msg">${item.msg}</div></div>`).join('');
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = `<button class="page-btn" ${currentPage === 1 ? 'disabled' : ''} onclick="changePage(-1)">이전</button><span class="page-info">${currentPage} / ${totalPages || 1}</span><button class="page-btn" ${currentPage === totalPages || totalPages === 0 ? 'disabled' : ''} onclick="changePage(1)">다음</button>`;
        }
        function changePage(offset) { currentPage += offset; loadGuestbook(); }
        function addGuestbook() {
            const name = document.getElementById('gb-name').value; const msg = document.getElementById('gb-msg').value;
            if (!name || !msg) return alert('성함과 메시지를 입력해주세요.');
            const list = JSON.parse(localStorage.getItem('wedding_gb') || '[]');
            list.push({ name, msg }); localStorage.setItem('wedding_gb', JSON.stringify(list));
            document.getElementById('gb-name').value = ''; document.getElementById('gb-msg').value = '';
            currentPage = 1; loadGuestbook();
        }
        window.onload = loadGuestbook;
    </script>
</body>
</html>
"""
    account_html = "".join([f'<div class="account-item"><div><strong>{a["owner"]}</strong><br><small style="color:#666;">{a["bank"]} {a["number"]}</small></div><button class="copy-btn" onclick="copyToClipboard(\'{a["number"].replace("-", "")}\')">복사</button></div>' for a in data['accounts']])
    
    html_content = template_text
    html_content = html_content.replace("{{groom_name}}", data['groom_name']).replace("{{bride_name}}", data['bride_name'])
    html_content = html_content.replace("{{wedding_date}}", data['wedding_date']).replace("{{wedding_time}}", data['wedding_time'])
    html_content = html_content.replace("{{hall_detail}}", data['hall_detail']).replace("{{address}}", data['address'])
    html_content = html_content.replace("{{greeting_title}}", data['greeting_title']).replace("{{greeting_message}}", data['greeting_message'])
    html_content = html_content.replace("{{cover_photo}}", cover_photo).replace("{{map_image_url}}", data['map_image_url'])
    html_content = html_content.replace("{{subway}}", data['transportation']['subway']).replace("{{bus}}", data['transportation']['bus']).replace("{{parking}}", data['transportation']['parking'])
    html_content = html_content.replace("{{wedding_year}}", data['wedding_date'].split('-')[0]).replace("{{account_items_html}}", account_html)
    html_content = html_content.replace("{{photo_data_json}}", json.dumps(data['photos']))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Deployment-ready invitation generated at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_invitation_html(MY_DATA)
    os.system(f"open index.html")
