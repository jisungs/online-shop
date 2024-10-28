document.addEventListener('DOMContentLoaded', function () {
    var IMP = window.IMP;
    IMP.init('imp11166264'); // 아임포트 고유 가맹점 식별코드

    document.querySelector('.order-form').addEventListener('submit', function (e) {
        e.preventDefault();

        var amount = parseFloat(document.querySelector('.order-form input[name="amount"]').value.replace(',', ''));
        var type = document.querySelector('.order-form input[name="type"]:checked').value;

        // 폼 데이터를 기준으로 주문 생성
        var order_id = AjaxCreateOrder(e);
        if (!order_id) {
            alert('주문 생성 실패\n다시 시도해주세요.');
            return;
        }

        // 결제 정보 생성
        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);

        // 결제 정보가 만들어졌으면 iamport로 실제 결제 시도
        if (merchant_id !== '') {
            IMP.request_pay({
                merchant_uid: merchant_id,
                name: 'E-Shop product',
                buyer_name: document.querySelector('input[name="first_name"]').value + " " + document.querySelector('input[name="last_name"]').value,
                buyer_email: document.querySelector('input[name="email"]').value,
                amount: amount
            }, function (rsp) {
                if (rsp.success) {
                    var msg = '결제가 완료되었습니다.';
                    msg += '\n고유ID : ' + rsp.imp_uid;
                    msg += '\n상점 거래ID : ' + rsp.merchant_uid;
                    msg += '\n결제 금액 : ' + rsp.paid_amount;
                    msg += '\n카드 승인번호 : ' + rsp.apply_num;

                    // 결제가 완료되었으면 비교해서 디비에 반영
                    ImpTransaction(e, order_id, rsp.merchant_uid, rsp.imp_uid, rsp.paid_amount);
                } else {
                    var msg = '결제에 실패하였습니다.\n';
                    msg += '에러내용 : ' + rsp.error_msg;
                    console.log(msg);
                }
            });
        }
    });
});

// 폼 데이터를 기준으로 주문 생성
function AjaxCreateOrder(e) {
    e.preventDefault();
    var order_id = '';

    fetch(order_create_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token
        },
        body: new URLSearchParams(new FormData(document.querySelector('.order-form')))
    })
    .then(response => response.json())
    .then(data => {
        if (data.order_id) {
            order_id = data.order_id;
        }
    })
    .catch(error => {
        if (error.status === 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (error.status === 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });

    return order_id;
}

// 결제 정보 생성
function AjaxStoreTransaction(e, order_id, amount, type) {
    e.preventDefault();
    var merchant_id = '';

    fetch(order_checkout_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token
        },
        body: new URLSearchParams({
            order_id: order_id,
            amount: amount,
            type: type
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.works) {
            merchant_id = data.merchant_id;
        }
    })
    .catch(error => {
        if (error.status === 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (error.status === 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });

    return merchant_id;
}

// iamport에 결제 정보가 있는지 확인 후 결제 완료 페이지로 이동
function ImpTransaction(e, order_id, merchant_id, imp_id, amount) {
    e.preventDefault();

    fetch(order_validation_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf_token
        },
        body: new URLSearchParams({
            order_id: order_id,
            merchant_id: merchant_id,
            imp_id: imp_id,
            amount: amount
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.works) {
            window.location.href = location.origin + order_complete_url + '?order_id=' + order_id;
        }
    })
    .catch(error => {
        if (error.status === 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (error.status === 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다. 다시 시도해주세요.");
        }
    });
}