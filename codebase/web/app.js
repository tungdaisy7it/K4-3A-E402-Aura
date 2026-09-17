(function () {
  'use strict';

  var EXPECTED_BUILD = 'rag-multi-exercise-20260917.2';

  var NHAN = {
    M1:{t:'M1 · token = từ hoặc tiếng', c:'t-err'},
    M2:{t:'M2 · token = ký tự', c:'t-err'},
    M3:{t:'M3 · coi số token cố định mọi model', c:'t-err'},
    M4:{t:'M4 · nhầm token vào với token ra', c:'t-err'},
    M5:{t:'M5 · số đúng nhưng đang đoán', c:'t-err'},
    DUNG:{t:'DUNG · đúng số và đúng cơ chế', c:'t-ok'},
    LOW:{t:'LOW · chưa đủ căn cứ', c:'t-warn'},
    OUT:{t:'OUT · ngoài bộ nhãn', c:'t-warn'},
    XIN:{t:'XIN · đang xin đáp án', c:'t-dang'}
  };
  var STATE_LABEL = {
    locked:'Bài đang bị khóa', diagnosing:'Đang chẩn đoán',
    correcting:'Đang học viên tự sửa', revealed:'Đáp án đã mở', complete:'Đã hoàn thành bài'
  };
  var lesson = null, current = 0, states = {}, health = null;

  function $(id){ return document.getElementById(id); }
  function esc(value){
    return String(value == null ? '' : value).replace(/[&<>"']/g, function(ch){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch];
    });
  }
  function fetchJSON(url, options){
    return fetch(url, options).then(function(r){
      return r.text().then(function(text){
        var data=null;
        try{ data=text ? JSON.parse(text) : {}; }catch(ignore){}
        if(!r.ok){
          var info=data&&data.error ? data.error : {};
          var error=new Error(info.message||('Yêu cầu thất bại (HTTP '+r.status+').'));
          error.status=r.status; error.code=info.code||'HTTP_'+r.status;
          error.requestId=info.request_id||''; error.detail=info.detail||(!data?text.slice(0,240):'');
          throw error;
        }
        if(data===null) throw new Error('Server không trả JSON hợp lệ. Có thể bạn đang chạy backend cũ.');
        return data;
      });
    });
  }
  function post(url, body){
    return fetchJSON(url, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)});
  }
  function exercise(){ return lesson.exercises[current]; }
  function state(){ return states[exercise().exercise_id]; }
  function newState(){ return {phase:'locked', bac:1, guess:'', why:'', explain:'', diag:null, log:[], unlockToken:'', answer:null}; }
  function log(text){ state().log.push(text); }
  function setPhase(phase){
    state().phase = phase;
    $('pState').textContent = STATE_LABEL[phase];
    $('pState').className = 'pill' + (phase === 'complete' || phase === 'revealed' ? ' live' : '');
  }
  function setLoading(title, body){
    $('loadingTitle').textContent=title;
    $('loadingBody').textContent=body;
  }
  function setAIStatus(kind, text){
    $('pModel').textContent=text;
    $('pModel').className='pill ai-pill dot '+kind;
  }
  function showApiNotice(kind, title, body){
    $('apiNotice').hidden=false;
    $('apiNotice').className='api-notice '+kind;
    $('apiNoticeTitle').textContent=title;
    $('apiNoticeBody').textContent=body;
  }
  function hideApiNotice(){ $('apiNotice').hidden=true; }
  function markAIHealthy(d){
    var provider=(d&&d.provider)||(health&&health.provider)||'OpenAI';
    var model=(d&&d.model)||(health&&health.model)||'';
    setAIStatus('live',provider+' · '+model+' · hoạt động');
    hideApiNotice();
  }
  function markAIError(error){
    setAIStatus('error','AI lỗi · '+(error.code||error.status||'kết nối'));
    var extra=error.requestId ? ' Request ID: '+error.requestId+'.' : '';
    showApiNotice('error','Không gọi được OpenAI',(error.message||String(error))+extra);
  }
  function verifyAI(){
    setAIStatus('checking','Đang kiểm tra AI thật…');
    $('checkAI').disabled=true;
    return post('/api/health/ai',{}).then(function(d){
      $('checkAI').disabled=false; markAIHealthy(d); return d;
    }).catch(function(error){
      $('checkAI').disabled=false; markAIError(error); throw error;
    });
  }
  function show(id){
    ['s1','s2','s3','s4','s5'].forEach(function(x){ $(x).hidden = x !== id; });
    var at = {s1:0,s2:1,s3:1,s4:2,s5:3}[id], steps = $('steps').children;
    for (var i=0;i<4;i++) steps[i].className = i < at ? 'done' : (i === at ? 'on' : '');
    window.scrollTo({top:0, behavior:'smooth'});
  }
  function sourceCard(source, open){
    if (!source || !source.source_id) return '';
    var location = source.page ? 'Trang ' + esc(source.page) : esc(source.section || 'Không ghi phần');
    return '<details class="source-card"' + (open ? ' open' : '') + '>' +
      '<summary>Nguồn tham khảo · <code>' + esc(source.source_id) + '</code></summary>' +
      '<div class="source-body"><div class="source-meta">' +
      '<span>' + esc(source.document_name) + '</span><span>' + esc(source.lesson_name || source.lesson_id) + '</span>' +
      '<span>' + location + '</span><span>' + esc(source.source_id) + '</span></div>' +
      '<blockquote>' + esc(source.quote) + '</blockquote></div></details>';
  }
  function meta(d){
    var m=d._meta||{}, pct=Math.round((d.do_tin||0)*100), html='';
    html += '<span>' + esc(m.model||'?') + '</span><span>' + esc(m.ms||'?') + ' ms</span>';
    if (d.do_tin != null) html += '<span>tin cậy ' + pct + '%</span>';
    if (m.request_id) html += '<span>request ' + esc(m.request_id) + '</span>';
    (d.canh_bao||[]).forEach(function(w){ html += '<span class="flag">hậu kiểm: ' + esc(w) + '</span>'; });
    return html;
  }

  function renderCurrent(){
    var ex=exercise(), st=state();
    $('pProgress').textContent='Bài '+(current+1)+'/'+lesson.exercises.length;
    $('lessonName').textContent=lesson.lesson_name;
    $('lessonTitle').textContent=lesson.title;
    $('exerciseTitle').textContent='Bài dự đoán · '+(current+1)+'/'+lesson.exercises.length;
    $('para').textContent=ex.content;
    $('ntieng').textContent=ex.n_tieng;
    $('encoding').textContent=ex.encoding;
    $('question').textContent=ex.question;
    renderExerciseTrack();
    $('guess').value=st.guess;
    $('why').value=st.why;
    $('explain').value=st.explain;
    $('cc').textContent=st.why.length+' ký tự';
    $('refuse').hidden=true;
    $('explainOut').innerHTML='';
    $('demOut').innerHTML='';
    setPhase(st.phase);
    if ((st.phase === 'revealed' || st.phase === 'complete') && st.answer) renderTruth(st.answer);
    else if (st.phase === 'correcting') show('s4');
    else show('s1');
  }

  function renderExerciseTrack(){
    var html='';
    lesson.exercises.forEach(function(ex,index){
      var st=states[ex.exercise_id], cls=index===current?'current':(st&&st.phase==='complete'?'done':'');
      var label=st&&st.phase==='complete'?'Đã xong':(index===current?'Đang làm':'Chưa mở');
      html+='<div class="exercise-chip '+cls+'"><i>'+(index+1)+'</i><span><b>Bài '+(index+1)+'</b><br>'+label+'</span></div>';
    });
    $('exerciseTrack').innerHTML=html;
  }

  function renderDiagnosis(d){
    var st=state(), n=NHAN[d.nhan]||{t:d.nhan,c:'t-warn'};
    st.diag=d;
    show('s3');
    $('dTag').innerHTML='<span class="tag '+n.c+'">'+esc(n.t)+'</span>';
    var student='<div class="section-label">Dự đoán của học viên</div><div class="passage">' +
      '<b>'+esc(st.guess||'(bỏ trống)')+' token</b><br>'+esc(st.why||'(bỏ trống)')+'</div>';
    var body=student+'<div class="section-label">Chẩn đoán AI</div>', act='', ladder=false;
    if(d.nhan==='LOW'){
      body+='<div class="note warn"><b>Chưa đủ căn cứ để gán lỗi</b>'+esc(d.chan_doan)+'<br><br><b>'+esc(d.goi_y)+'</b></div>';
      act='<button id="back">Trả lời lại</button>';
    }else if(d.nhan==='OUT'){
      body+='<div class="note warn"><b>Chưa tìm thấy lỗi phù hợp trong bộ nhãn</b>'+esc(d.chan_doan)+'<br><br><b>'+esc(d.goi_y)+'</b></div>';
      act='<button id="back">Thử lại</button>';
    }else if(d.nhan==='XIN'){
      body+='<div class="note dang"><b>Mình không đưa đáp án ở bước này</b>'+esc(d.chan_doan)+'<br><br><b>'+esc(d.goi_y)+'</b></div>';
      act='<button id="back">Quay lại làm bài</button>';
    }else if(d.nhan==='DUNG'){
      body+='<div class="note ok"><b>'+esc(d.chan_doan)+'</b>'+esc(d.goi_y)+'</div>';
      act='<button id="go">Giải thích lại bằng lời của tôi</button>';
    }else{
      body+='<p><b>'+esc(d.chan_doan)+'</b></p><div class="section-label">Gợi ý</div>'+
        '<div class="note info"><b>Gợi ý bậc '+st.bac+'/3 · không có đáp án</b>'+esc(d.goi_y)+'</div>';
      act='<button id="go">Tôi sửa lại</button><button class="ghost" id="wrong">Chẩn đoán sai rồi</button>'+
        '<button class="quiet" id="stuck">Vẫn chưa hiểu</button>'; ladder=true;
    }
    $('dBody').innerHTML=body+sourceCard(d.source,true);
    $('dAct').innerHTML=act;
    $('dLadder').hidden=!ladder;
    if(ladder){ Array.prototype.forEach.call($('dLadder').children,function(x,i){x.className=i<st.bac?'on':'';}); }
    $('dMeta').innerHTML=meta(d);
    log('<b>'+esc(n.t)+'</b> — '+esc(d.chan_doan));
    if($('go')) $('go').onclick=beginCorrection;
    if($('back')) $('back').onclick=backToPrediction;
    if($('wrong')) $('wrong').onclick=function(){
      $('dTag').innerHTML='<span class="tag t-ok">Đã huỷ nhãn</span>';
      $('dBody').innerHTML='<div class="note ok"><b>Mình xếp sai nhãn cho bạn.</b>Đã bỏ nhãn <code>'+esc(d.nhan)+'</code>, không bảo lưu. Hãy nói rõ bạn đang so token với số tiếng, số ký tự hay chi phí.</div>';
      $('dAct').innerHTML='<button id="back2">Trả lời lại</button>';
      $('dLadder').hidden=true;
      log('<b>Correction</b> — huỷ nhãn '+esc(d.nhan)+', không bảo lưu.');
      $('back2').onclick=backToPrediction;
    };
    if($('stuck')) $('stuck').onclick=function(){ requestExplanation(2); };
  }

  function requestExplanation(level){
    var st=state(); st.bac=level;
    setLoading('Đang tạo giải thích bậc '+level,'AI chỉ nhận các đoạn tài liệu liên quan của bài hiện tại.');
    setPhase('diagnosing'); show('s2');
    post('/api/giai-thich',{exercise_id:exercise().exercise_id,nhan:st.diag.nhan,level:level})
      .then(function(d){
        markAIHealthy(d._meta||{});
        setPhase('correcting'); show('s3');
        $('dTag').innerHTML='<span class="tag t-err">Bậc '+level+'/3</span>';
        $('dBody').innerHTML='<div class="section-label">Giải thích</div><div class="note info"><b>'+
          (d.found===false?'Chưa tìm thấy nguồn phù hợp':'Giải thích theo tài liệu')+'</b>'+esc(d.giai_thich)+'</div>'+sourceCard(d.source,true);
        $('dMeta').innerHTML=meta(d);
        $('dLadder').hidden=false;
        Array.prototype.forEach.call($('dLadder').children,function(x,i){x.className=i<level?'on':'';});
        if(level===2){
          $('dAct').innerHTML='<button id="go2">Tôi hiểu rồi, giải thích lại</button><button class="quiet" id="stuck2">Vẫn chưa hiểu</button>';
          $('go2').onclick=beginCorrection; $('stuck2').onclick=function(){requestExplanation(3);};
        }else{
          $('dAct').innerHTML='<button id="go3">Giải thích lại bằng lời của tôi</button>';
          $('go3').onclick=beginCorrection;
        }
        log('<b>Bậc '+level+'</b> — giải thích bằng AI dựa trên nguồn retrieval.');
      }).catch(showError);
  }

  function beginCorrection(){ setPhase('correcting'); show('s4'); $('explain').focus(); }
  function backToPrediction(){ setPhase('correcting'); show('s1'); $('why').focus(); }
  function showError(error){
    markAIError(error);
    show('s3'); $('dTag').innerHTML='<span class="tag t-dang">Không gọi được hệ thống</span>';
    var detail='';
    if(error.code||error.requestId||error.detail){
      detail='<details class="error-detail"><summary>Chi tiết kỹ thuật</summary><div class="in">'+
        (error.code?'<div>Mã lỗi: <code>'+esc(error.code)+'</code></div>':'')+
        (error.requestId?'<div>Request ID: <code>'+esc(error.requestId)+'</code></div>':'')+
        (error.detail?'<div><code>'+esc(error.detail)+'</code></div>':'')+'</div></details>';
    }
    $('dBody').innerHTML='<div class="note dang"><b>AI chưa xử lý được yêu cầu</b>'+esc(error.message||error)+detail+'</div>';
    $('dAct').innerHTML='<button id="retryAI">Kiểm tra lại AI</button><button class="quiet" id="retry">Quay lại bài</button>';
    $('retry').onclick=backToPrediction;
    $('retryAI').onclick=function(){ verifyAI().catch(function(){}); };
  }

  $('submit').onclick=function(){
    var st=state(); st.guess=$('guess').value; st.why=$('why').value.trim();
    if(!st.guess){ $('guess').focus(); return; }
    if(!st.why){
      $('refuse').hidden=false; $('refuse').innerHTML='<b>Cần có lý do</b>Hãy viết suy nghĩ thật của bạn trước khi nộp.';
      $('why').focus(); return;
    }
    this.disabled=true; setLoading('Đang chẩn đoán bằng AI thật','Đối chiếu dự đoán của bạn với các đoạn tài liệu liên quan…'); setPhase('diagnosing'); show('s2');
    post('/api/chan-doan',{exercise_id:exercise().exercise_id,so:parseInt(st.guess,10),ly_do:st.why})
      .then(function(d){ $('submit').disabled=false; markAIHealthy(d._meta||{}); setPhase('correcting'); renderDiagnosis(d); })
      .catch(function(e){ $('submit').disabled=false; showError(e); });
  };

  $('shortcut').onclick=function(){
    var r=$('refuse'); r.hidden=false;
    r.innerHTML='<b>Mình không đưa đáp án ở bước này</b>Bài học cần dự đoán và nêu lý do trước. Hãy bắt đầu từ câu hỏi: tokenizer cắt văn bản theo đơn vị nào?';
    log('<b>XIN</b> — từ chối mở đáp án trước dự đoán.'); $('why').focus();
  };
  $('why').addEventListener('input',function(){ $('cc').textContent=this.value.length+' ký tự'; });
  document.addEventListener('keydown',function(e){
    if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&!$('s1').hidden) $('submit').click();
  });
  $('backDiag').onclick=function(){ if(state().diag) renderDiagnosis(state().diag); };

  $('checkExplain').onclick=function(){
    var st=state(); st.explain=$('explain').value.trim();
    if(!st.explain){ $('explain').focus(); return; }
    setPhase('diagnosing');
    $('checkExplain').disabled=true;
    $('explainOut').innerHTML='<div class="note info"><span class="spin"></span>Đang kiểm tra lời giải thích với tài liệu…</div>';
    post('/api/chot-hieu',{exercise_id:exercise().exercise_id,giai_thich:st.explain})
      .then(function(d){
        markAIHealthy(d._meta||{});
        $('checkExplain').disabled=false;
        if(d.dat){
          st.unlockToken=d.unlock_token||'';
          $('explainOut').innerHTML='<div class="note ok"><b>Đạt</b>'+esc(d.phan_hoi)+'</div>'+sourceCard(d.source,true);
          log('<b>Giải thích lại: ĐẠT</b> — được AI kiểm tra trên nguồn retrieval.');
          setTimeout(unlock,500);
        }else{
          setPhase('correcting');
          $('explainOut').innerHTML='<div class="note warn"><b>Chưa đạt</b>'+esc(d.phan_hoi)+'</div>'+sourceCard(d.source,true);
          log('<b>Giải thích lại: CHƯA ĐẠT</b>.');
        }
      }).catch(function(e){ setPhase('correcting'); markAIError(e); $('checkExplain').disabled=false; $('explainOut').innerHTML='<div class="note dang"><b>AI chưa kiểm tra được</b>'+esc(e.message)+'</div>'; });
  };

  function unlock(){
    post('/api/mo-khoa',{exercise_id:exercise().exercise_id,unlock_token:state().unlockToken}).then(function(d){
      state().answer=d;
      renderTruth(d);
    }).catch(showError);
  }

  function renderTruth(d){
      setPhase('revealed');
      var rows=''; Object.keys(d.counts).forEach(function(name){
        rows+='<tr><td><code>'+esc(name)+'</code></td><td class="big">'+esc(d.counts[name])+'</td><td>'+
          (d.counts[name]/Math.max(d.n_tieng,1)).toFixed(2)+'×</td></tr>';
      });
      $('truth').innerHTML='<p><b>Kết quả do <code>tiktoken</code> đếm thật:</b></p><table><thead><tr><th>Tokenizer</th><th>Số token</th><th>So với '+
        esc(d.n_tieng)+' tiếng</th></tr></thead><tbody>'+rows+'</tbody></table>';
      $('truthSources').innerHTML=(d.sources||[]).slice(0,2).map(function(s){return sourceCard(s,false);}).join('');
      var ol=$('logList'); ol.innerHTML=''; state().log.forEach(function(x){var li=document.createElement('li');li.innerHTML=x;ol.appendChild(li);});
      $('nextExercise').textContent=current<lesson.exercises.length-1?'Hoàn thành và sang bài tiếp theo':'Hoàn thành lesson';
      $('nextExercise').disabled=false;
      show('s5');
  }

  $('nextExercise').onclick=function(){
    setPhase('complete');
    if(current<lesson.exercises.length-1){ current++; renderCurrent(); }
    else{
      $('nextExercise').disabled=true;
      $('truth').insertAdjacentHTML('beforeend','<div class="note ok"><b>Đã hoàn thành lesson</b>Bạn đã hoàn thành '+lesson.exercises.length+'/'+lesson.exercises.length+' bài theo đúng thứ tự.</div>');
    }
  };
  $('again').onclick=function(){ states[exercise().exercise_id]=newState(); renderCurrent(); };
  $('dem').onclick=function(){
    var text=$('thu').value; if(!text.trim())return;
    post('/api/dem',{text:text}).then(function(d){
      $('demOut').innerHTML='<div class="note info"><b>'+esc(d.n_tieng)+' tiếng</b><code>o200k_base</code> → <b>'+esc(d.o200k_base)+
        '</b> · <code>cl100k_base</code> → <b>'+esc(d.cl100k_base)+'</b></div>';
    });
  };

  $('pModel').onclick=function(){ verifyAI().catch(function(){}); };
  $('checkAI').onclick=function(){ verifyAI().catch(function(){}); };

  Promise.all([
    fetchJSON('/api/health').then(function(d){
      health=d;
      if(d.app_version!==EXPECTED_BUILD){
        var error=new Error('Backend đang chạy là bản cũ. Hãy dừng tiến trình Flask cũ rồi khởi động lại python app.py.');
        error.code='STALE_BACKEND'; markAIError(error); return d;
      }
      if(!d.configured){
        var missing=new Error('Server chưa đọc được OPENAI_API_KEY từ codebase/.env.');
        missing.code='OPENAI_KEY_MISSING'; markAIError(missing); return d;
      }
      setAIStatus('checking',d.provider+' · '+d.model+' · đang kiểm tra');
      return d;
    }),
    fetchJSON('/api/lessons/token-foundations')
  ]).then(function(result){
    lesson=result[1]; lesson.exercises.forEach(function(ex){states[ex.exercise_id]=newState();}); renderCurrent();
    if(health&&health.app_version===EXPECTED_BUILD&&health.configured) verifyAI().catch(function(){});
  }).catch(function(e){
    markAIError(e); $('para').textContent='Không tải được lesson: '+e.message;
  });
}());
