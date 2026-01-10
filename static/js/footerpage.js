document.addEventListener('DOMContentLoaded', function() {
  if (typeof tinymce === 'undefined') return;
  const selector = 'textarea.tinymce';
  if (!document.querySelector(selector)) return;
  tinymce.init({
    selector,
    height: 500,
    menubar: true,
    plugins: 'advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table help wordcount paste',
    toolbar: 'undo redo | blocks | bold italic underline | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image table | insertProTip insertNote | removeformat | preview code fullscreen',
    content_css: false,
    branding: false,
    convert_urls: false,
    image_title: true,
    automatic_uploads: true,
    file_picker_types: 'image',
    paste_data_images: true,
    images_upload_handler: function (blobInfo, success, failure) {
      const formData = new FormData();
      formData.append('file', blobInfo.blob(), blobInfo.filename());
      fetch('/editor/upload/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        body: formData,
        credentials: 'same-origin'
      }).then(r => r.ok ? r.json() : Promise.reject())
        .then(data => data && data.location ? success(data.location) : failure('Upload error'))
        .catch(() => failure('Upload failed'));
    },
    block_formats: 'Paragraph=p; Heading 1=h1; Heading 2=h2; Heading 3=h3; Heading 4=h4',
    content_style: `
      body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; font-size:16px; line-height:1.85; color:#111827; }
      h1, h2, h3, h4 { color:#0F3C7A; font-weight:800; margin:16px 0 10px; line-height:30px; }
      h1 { font-size:22px; }
      h2 { font-size:20px; }
      h3 { font-size:18px; }
      h4 { font-size:17px; }
      p { margin:8px 0 18px; color:#374151; text-align:justify; }
      ul, ol { margin:0 0 16px 20px; }
      li { margin:4px 0; }
      a { color:#1d4ed8; text-decoration:underline; }
      strong { font-weight:600; }
      .ai-protip{ border:1px solid #bfdbfe; background:#eff6ff; color:#0c4a6e; border-radius:16px; padding:16px; margin:16px 0; }
      .ai-protip::before{ content:"PRO TIP"; display:block; font-weight:800; letter-spacing:.02em; margin-bottom:6px; color:#1e3a8a; }
      .ai-note{ border:1px solid #bfdbfe; background:#eff6ff; color:#0c4a6e; border-radius:12px; padding:12px; margin:12px 0; }
      .ai-note::before{ content:"Note"; display:block; font-weight:600; margin-bottom:4px; color:#1e3a8a; }
    `
    ,file_picker_callback: function (cb, value, meta) {
      if (meta.filetype !== 'image') return;
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.onchange = function () {
        const file = this.files[0];
        const formData = new FormData();
        formData.append('file', file, file.name);
        fetch('/editor/upload/', {
          method: 'POST',
          headers: { 'X-CSRFToken': getCookie('csrftoken') },
          body: formData,
          credentials: 'same-origin'
        }).then(r => r.ok ? r.json() : Promise.reject())
          .then(data => data && data.location ? cb(data.location, { title: file.name }) : null)
          .catch(() => {});
      };
      input.click();
    }
    ,setup(editor){
      function wrapWith(tag){
        const selHtml = (editor.selection.getContent({format:'html'}) || '').trim();
        const selText = (editor.selection.getContent({format:'text'}) || '').trim();
        const base = selHtml || tinymce.util.Entities.encodeAllRaw(selText);
        const content = base || (tag==='protip' ? 'Yahan apna pro tip likhen' : 'Yahan apna note likhen');
        const cls = tag==='protip' ? 'ai-protip' : 'ai-note';
        editor.insertContent(`<div class="${cls}">${content}</div>`);
      }
      editor.ui.registry.addButton('insertProTip',{
        text:'Pro Tip',
        tooltip:'Insert Pro Tip',
        onAction:()=>wrapWith('protip')
      });
      editor.ui.registry.addButton('insertNote',{
        text:'Note',
        tooltip:'Insert Note',
        onAction:()=>wrapWith('note')
      });
      editor.ui.registry.addMenuItem('insertProTip',{
        text:'Insert Pro Tip',
        onAction:()=>wrapWith('protip')
      });
      editor.ui.registry.addMenuItem('insertNote',{
        text:'Insert Note',
        onAction:()=>wrapWith('note')
      });
    }
  });
  function slugify(str) {
    return String(str).toLowerCase().trim()
      .replace(/[\s\-_]+/g, '-')
      .replace(/[^a-z0-9\-]/g, '')
      .replace(/\-+/g, '-');
  }
  const titleEl = document.getElementById('id_title');
  const linkEl = document.getElementById('id_link');
  const metaTitleEl = document.getElementById('id_meta_title');
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }
  if (titleEl && linkEl) {
    const updateLink = () => {
      const s = slugify(titleEl.value || '');
      if (s) {
        if (linkEl.value === '' || linkEl.value.startsWith('/pages/')) {
          linkEl.value = `/pages/${s}/`;
        }
        if (metaTitleEl && (metaTitleEl.value === '' || metaTitleEl.value === titleEl.dataset.prevTitle)) {
          metaTitleEl.value = titleEl.value;
        }
      }
      titleEl.dataset.prevTitle = titleEl.value;
    };
    titleEl.addEventListener('input', updateLink);
    titleEl.addEventListener('change', updateLink);
  }
});
