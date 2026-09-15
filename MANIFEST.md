# 이미지 추가와 자동 목록

## 파일 추가

`public/match_images/{male|female}/{wood|fire|earth|metal|water}_{번호}.png` 형태로 추가합니다.
예: `public/match_images/male/fire_06.png`.

main에 PNG를 추가/삭제하면 GitHub Actions가 `public/match_images/manifest.json`을 갱신합니다. 앱은 목록의 성별·오행이 맞는 이미지 중 랜덤으로 선택합니다. 앱에는 이 목록을 읽는 변경을 한 번 배포해야 합니다.

기존 미사용 `_05` 파일은 `scripts/excluded_images.json`에 명시적으로 제외했습니다. 사용 승인 후 해당 줄을 제거하면 됩니다. 새 번호는 이 제외 목록에 없으면 자동 포함됩니다.

## 로컬 검증/생성

```sh
python3 scripts/test_generate_manifest.py
python3 scripts/generate_manifest.py
```

외부 패키지는 필요 없습니다. 재실행 시 내용이 같으면 파일을 다시 쓰지 않습니다. 생성기는 PNG 파일명/경로를 검사하며 이미지 내용 검수는 별도로 수행해야 합니다.

## 운영 확인

- Actions 완료 및 raw manifest 응답을 확인합니다. 캐시 때문에 업로드 순간 즉시 모든 기기에 나타나는 것은 아닙니다.
- 앱은 목록 조회 실패·빈 그룹일 때 기존 01~03 선택 방식으로 돌아갑니다.
- main 보호 규칙으로 Actions 쓰기가 막히면 권한을 임의 우회하지 말고, 로컬 생성한 manifest를 정상 PR로 반영합니다.
- 동시 push로 자동 커밋이 거절되면 해당 작업을 재실행합니다. 강제 push는 하지 않습니다.
- 이 작업은 로컬 구현/검증 상태입니다. workflow/manifest 원격 반영과 Toss 앱 배포는 별도 승인 단계입니다.
