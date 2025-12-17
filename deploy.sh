#!/bin/bash
# Skripta za automatski deploy na PythonAnywhere
# Koristi Git push + PythonAnywhere API reload

echo "🚀 PythonAnywhere Auto-Deploy"
echo ""

# Proveri da li postoje promene
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Pronađene promene:"
    git status --short
    echo ""
    read -p "Da li želiš da commit-uješ i push-uješ promene? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Unesi commit poruku: " commit_msg
        if [ -z "$commit_msg" ]; then
            commit_msg="Auto-deploy from Cursor"
        fi
        
        git add .
        git commit -m "$commit_msg"
        git push
        
        echo "✅ Promene su push-ovane na GitHub"
    fi
else
    echo "ℹ️  Nema promena za commit"
fi

# Reload PythonAnywhere (ako su postavljene environment varijable)
if [ -n "$PYTHONANYWHERE_USERNAME" ] && [ -n "$PYTHONANYWHERE_API_TOKEN" ]; then
    echo ""
    echo "🔄 Reload-ujem aplikaciju na PythonAnywhere..."
    curl -X POST \
        -H "Authorization: Token $PYTHONANYWHERE_API_TOKEN" \
        https://www.pythonanywhere.com/api/v0/user/$PYTHONANYWHERE_USERNAME/webapps/$PYTHONANYWHERE_USERNAME.pythonanywhere.com/reload/
    
    if [ $? -eq 0 ]; then
        echo "✅ Aplikacija je reload-ovana"
    else
        echo "❌ Greška pri reload-u"
    fi
else
    echo ""
    echo "⚠️  Environment varijable nisu postavljene"
    echo "💡 Postavi PYTHONANYWHERE_USERNAME i PYTHONANYWHERE_API_TOKEN"
fi

