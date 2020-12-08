# dltools
DeepLabel 지원을 위한 툴
# Install
- python 3.7 이상에서 테스트 완료
```bash
pip install cython
pip install git+https://github.com/zmfkzj/dltools.git
```
# 사용준비
1. DeepLabel에서 dump 혹은 export로 annotation 다운로드
1. 새로운 폴더를 만들어 다운로드 받은 데이터셋 이동
1. 새폴더 안의 데이터셋을 각 폴더에 압축풀기
# 사용법
1. 명령 프롬프트 혹은 터미널 실행
1. dltools + `Enter`로 실행
1. 폴더 선택창에서 [사용준비](#사용준비)에서 만든 새폴더 선택
1. 원하는 메뉴의 No를 선택 후 `Enter`
1. 안내에 따라 옵션 입력
## 데이터셋 합치기
새폴더의 부모폴더 안에 merged 폴더가 생성되며 그 안에 결과물이 위치
## 데이터셋 변환
새폴더의 부모폴더 안에 export 폴더가 생성되며 그 안에 결과물이 위치
## 데이터셋 변환
새폴더 안의 각 데이터셋 안에 images_draw-object 폴더가 생성되며 그 안에 결과물 위치
