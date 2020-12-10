# dltools
DeepLabel 지원을 위한 툴
# Install
- windows10, python 3.7 이상에서 테스트 완료
- window에서 visual C++ 14.0 필요
  - [visual studio](https://visualstudio.microsoft.com/ko/downloads/) 최신버전 설치 후 C++ 개발도구 설치
- 명령 프롬프트에서 다음 커맨드 실행
```bash
pip install git+https://github.com/zmfkzj/dltools.git
```
# 사용준비
1. DeepLabel에서 dump 혹은 export로 annotation 다운로드(모두 같은 형식이어야 함)
1. 새로운 폴더를 만들어 다운로드 받은 데이터셋 이동
1. 새폴더 안의 데이터셋을 각 폴더에 압축풀기
# 사용법
1. 명령 프롬프트 혹은 터미널 실행
1. dltools + `Enter`로 실행
1. 폴더 선택창에서 [사용준비](#사용준비)에서 만든 새폴더 선택
1. 원하는 메뉴의 No를 선택 후 `Enter`
1. 안내에 따라 옵션 입력
## 데이터셋 합치기
- 여러 데이터셋(각 task에서 dump한 결과물)을 하나로 합침
- 새폴더의 부모폴더 안에 export/merged 폴더가 생성되며 그 안에 결과물이 위치
- 각 데이터셋의 images 폴더부터 파일명 까지가 그 이미지의 고유 id이며, 만약 id가 겹칠 경우 annotation이 합쳐짐
  ex)
  - `dataset1/images/foo/bar.jpg`이 id는 `foo/bar`
  - `dataset2/images/foo/bar.jpg`역시 id는 `foo/bar`로 위와 같음
  - 위 두 데이터셋을 합칠 경우 두 annotation의 내용이 합쳐짐
## 데이터셋 변환
- 새폴더의 부모폴더 안에 export 폴더가 생성되며 그 안에 결과물 위치
## Bounding box 그리기
- 새폴더 안의 각 데이터셋 안에 images_draw-label 폴더가 생성되며 그 안에 결과물 위치
